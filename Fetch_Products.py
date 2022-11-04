from bs4 import BeautifulSoup as BS
from selenium import webdriver
from html.parser import HTMLParser
import time, re
from Format_Data import reduce_tags

""" Options """

# path to chromedriver for selenium and headers to be used.
path_driver = "Order_Simulator/chromedriver-2"
Headers_data = ({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# frequently used regex compiler
nums = re.compile(r"[+-]?\d+(?:\,\d+)?")
euros = re.compile(r"€\d*[\.|\,]\d*|\d*[\.|\,]\d*€")
letters = re.compile(r"[A-Za-z]+")

# convert prices on page to float.
def convert_price(price: str) -> float:
    return float(euros.findall(price)[0].replace(",", ".").replace("€", ""))

""" Webdriver Selenium """

# get page via selenium.
def get_page_selenium(url):
    driver = webdriver.Chrome(path_driver)
    driver.get(url)

    # parse page via htmlparser.
    parser = HTMLParser()
    parser.feed(driver.page_source)
    page_html = driver.page_source

    # quit driver to close tab.
    driver.quit()
    return page_html

""" Classes """

class Product_Driver:
    """ Enter product that should be scraped """
    def __init__(self, category: str, url: str, perf: bool = False) -> None:
        self.category = category
        self.url = url
        self.time = None

        # if you want to see the time, use perf = True.
        if perf: self.time = time.perf_counter()

        # read page via selenium.
        page = get_page_selenium(self.url)  
        self.product_content = BS(page, features="html.parser")

        if self.time != None: print(f"read page in {time.perf_counter() - self.time} sec")

    # get title from the product page.
    def Get_Title(self):
        # some pages have diffrent formats, so try the most common ones.
        title_cache = self.product_content.find("span", id="productTitle")
        if title_cache == None: 
            title_cache = self.product_content.find("span", id="titleSection") 
        elif title_cache == None: 
            # if format of the page is not common, use None.
            self.name = "None"
            print("couldn't catch title")
            return None

        # add title to Product.
        self.name = title_cache.text.translate({ord("ß"):"ss"}).translate({ord(";"): None}).strip()
        self.hash = hash(self.url)

    # get product rating from the page. format will be [#rating, [#5star, #4start, etc.]].
    def Get_Rating_Info(self):
        rating_distribution = []
        # find rating in span.
        rating_cache = self.product_content.find("span", {"class": "cr-widget-Histogram"})
        if rating_cache != None:
            # get the rating from the table.
            rating_cache = rating_cache.findAll("table", id="histogramTable")[1].findAll("tr")
            for stars in rating_cache:
                rating_distribution.append(int(nums.findall(stars.text)[1]))

        # get number of total ratings. 
        rating_cache = self.product_content.find("div", {"class": "a-row a-spacing-medium averageStarRatingNumerical"}).text
        total_rating = int(nums.findall(rating_cache)[0].translate({ord(","): None}))
        
        # set product.rating to the before mentioned format.
        self.rating = [total_rating, rating_distribution]

    # get the price from the page
    def Get_Prices(self):
        # get div form page.
        price_cache = self.product_content.find("div", id="corePriceDisplay_desktop_feature_div")
        if price_cache == None:
            price_cache = self.product_content.find("table", {"class": "a-lineitem a-align-top"})
        price_pay = price_cache.find("span", {"class": "a-offscreen"})

        # convert price.
        self.price = convert_price(price_pay.text)

        # if there is a discount, then it will be added.
        price_sugg = price_cache.find("span", {"class": "a-size-small a-color-secondary aok-align-center basisPrice"})
        if price_sugg == None: self.sugg_price = 0
        else: self.sugg_price = convert_price(price_sugg.text)

    def Get_Tags(self):
        # get words in title.
        comp_title = self.name.split(" ")
        comp_title = [letters.findall(x) for x in comp_title]
        comp_title = [x[0] for x in comp_title if len(x) > 0]
        comp_title = ",".join(comp_title)

        # reduce tags.
        comp_title = str(reduce_tags(comp_title)).strip("[]").translate({ord("'"): None}).translate({ord(" "): None})
        self.tags = comp_title

    def Smartphone_Size(self):
        # find table on page.
        self.size = 0
        display_size = self.product_content.findAll("table", {"class": "a-bordered"})
        if len(display_size) > 2:
            # find td in table.
            display_size = display_size[1].findAll("tr")[0]
            display_size = display_size.findAll("td")[1].text
            display_size = nums.findall(display_size)[0].replace(",", ".")
            self.size = float(display_size)

    "To be added."

    def Headphone_NC(self):
        self.noise_canceling = None

    def TV_Size(self):
        self.size = None

    def Computer_Ram(self):
        self.ram = None

    def Get_Special_Attr(self):
        if self.category== "Smartphone": self.Smartphone_Size()
        elif self.category  == "Headphone": self.Headphone_NC()
        elif self.category  == "TV": self.TV_Size()
        elif self.category == "Computer": self.Computer_Ram()

    # Run this to get all the values.
    def Get_Data(self):
        self.Get_Title()
        self.Get_Prices()
        self.Get_Rating_Info()
        self.Get_Tags()
        self.Get_Special_Attr()

        if self.time != None: print(f"-> got attributes in {time.perf_counter() - self.time}")



if __name__ == "__main__":
    start = time.perf_counter()

    url_test = "https://www.amazon.de/MPVA3ZD-A/dp/B0BDJC83QY/ref=sr_1_1_sspa?crid=3MXI5609W6NW2&keywords=iphone&qid=1667246474&qu=eyJxc2MiOiI2LjgzIiwicXNhIjoiNi45OCIsInFzcCI6IjYuNDgifQ%3D%3D&sprefix=iphon%2Caps%2C142&sr=8-1-spons&psc=1"
    test = Product_Driver("Smartphone", url_test, True)
    test.Get_Data()
    
    print(f"Product:")
    for var in vars(test):
        if var != "product_content":
            print(f"{var}: {vars(test)[var]}")
    
    print(f"Done scraping products in {time.perf_counter() - start} sec.")