from bs4 import BeautifulSoup as BS
from selenium import webdriver
from html.parser import HTMLParser
import time, re
from Format_Data import reduce_tags
from Produktklassen_abc import Product, Smartphone, Headphone, TV, Computer

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

class Product_Driver:
    """ Enter product that should be scraped """
    def __init__(self, category: Product, perf: bool = False) -> None:
        self.category = category
        # if you want to see the time, use perf = True.
        if perf: 
            self.perf = perf
            self.time = time.perf_counter()
        # read page via selenium.
        page = get_page_selenium(category.url)  
        self.product_content = BS(page, features="html.parser")
    
        if self.perf: print(f"read page in {time.perf_counter() - self.time} sec")

    # get title from the product page.
    def Get_Title(self):
        # some pages have diffrent formats, so try the most common ones.
        title_cache = self.product_content.find("span", id="productTitle")
        if title_cache == None: 
            title_cache = self.product_content.find("span", id="titleSection") 
        elif title_cache == None: 
            # if format of the page is not common, use None.
            self.category.name = "None"
            print("couldn't catch title")
            return None
        # add title to Product.
        self.category.name = title_cache.text.translate({ord("ß"):"ss"}).strip()
        self.category.hash = hash(self.category.url)

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
        self.category.rating = [total_rating, rating_distribution]

    # get the price from the page
    def Get_Prices(self):
        # get div form page.
        price_cache = self.product_content.find("div", id="corePriceDisplay_desktop_feature_div")
        if price_cache == None:
            price_cache = self.product_content.find("table", {"class": "a-lineitem a-align-top"})
        price_pay = price_cache.find("span", {"class": "a-offscreen"})
        # convert price.
        self.category.price = convert_price(price_pay.text)
        # if there is a discount, then it will be added.
        price_sugg = price_cache.find("span", {"class": "a-size-small a-color-secondary aok-align-center basisPrice"})
        if price_sugg == None: 
            self.category.sugg_price = 0
        else: 
            self.category.sugg_price = convert_price(price_sugg.text)

    def Get_Tags(self):
        # split title.
        comp_title = self.category.name.split(" ")
        # get words in title.
        comp_title = [letters.findall(x) for x in comp_title]
        comp_title = [x[0] for x in comp_title if len(x) > 0]
        comp_title = ",".join(comp_title)
        # reduce tags.
        comp_title = str(reduce_tags(comp_title)).strip("[]").translate({ord("'"): None}).translate({ord(" "): None})
        self.category.tags = comp_title

    def Smartphone_Size(self):
        # find table on page.
        display_size = self.product_content.findAll("table", {"class": "a-bordered"})
        if len(display_size) > 2:
            # find td in table.
            display_size = display_size[1].findAll("tr")[0]
            display_size = display_size.findAll("td")[1].text
            display_size = nums.findall(display_size)[0].replace(",", ".")
            self.category.size = float(display_size)

    def Headphone_NC(self):
        pass

    def TV_Size(self):
        pass

    def Computer_Ram(self):
        pass

    def Get_Data(self):
        self.Get_Title()
        self.Get_Prices()
        self.Get_Rating_Info()
        self.Get_Tags()
        if self.perf: print(f"got attributes in {time.perf_counter() - self.time}")
        if self.category.category == "Smartphone":
            self.Smartphone_Size()
        elif self.category.category  == "Headphone":
            self.Headphone_NC()
        elif self.category.category  == "TV":
            self.TV_Size()
        elif self.category.category  == "Computer":
            self.Computer_Ram()

        if self.perf: print(f"finished in {time.perf_counter() - self.time}")

if __name__ == "__main__":
    start = time.perf_counter()
    print("start")
    test_smartphone_1 = Smartphone("https://www.amazon.de/MPXV3ZD-A/dp/B0BDJ61GFY/ref=sr_1_1_sspa?keywords=iphone+14+pro&qid=1666708676&qu=eyJxc2MiOiIzLjg5IiwicXNhIjoiMy41OSIsInFzcCI6IjMuMjQifQ%3D%3D&sprefix=ip%2Caps%2C119&sr=8-1-spons&psc=1")
    test_smartphone_2 = Smartphone("https://www.amazon.de/-/en/dp/B0BDJMH6JP?ref=ods_ucc_kindle_B0BDJMH6JP_rc_nd_ucc")
    test_smartphone_3 = Smartphone("https://www.amazon.de/GALAXY-S732GB-SI-A-36-Samsung-silver/dp/B0716T91X6/ref=sr_1_1_sspa?crid=1YRNH17UGYDOM&keywords=samsung+sma&qid=1666714844&qu=eyJxc2MiOiIxLjk4IiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&sprefix=samsung+sma%2Caps%2C115&sr=8-1-spons&psc=1")
    test_computer = Computer("https://www.amazon.de/-/en/Apple-MacBook-Air-chip-inch/dp/B08N5R7XXZ/ref=sr_1_4?crid=39XA1V7NDAML2&keywords=mac&qid=1666708761&qu=eyJxc2MiOiI1LjM3IiwicXNhIjoiNS42NyIsInFzcCI6IjUuMzEifQ%3D%3D&sprefix=mac%2Caps%2C109&sr=8-4")
    """
    # test computer.
    test = Product_Driver(test_computer, True)
    test.Get_Data()
    print(vars(test.category), "\n")

    # test smartphones. 
    for item in [test_smartphone_1, test_smartphone_2, test_smartphone_3]:
        test = Product_Driver(item, perf = True)
        test.Get_Data()
        print(vars(test.category), "\n")
    """
    print(f"{time.perf_counter() - start} sec.")