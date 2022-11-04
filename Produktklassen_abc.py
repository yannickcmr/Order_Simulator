from abc import ABC, abstractmethod
import io, os, codecs, sys, time
from Fetch_Products import Product_Driver

Path_Saving = "Test/"
try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  

""" Classes """

class Product(ABC):
	"Class of the products"
	def __init__(self, url: str) -> None:
		self.url = url
		self.category = None
		self.name = None
		self.price = None
		self.sugg_price = None
		self.rating = None
		self.hash = None
		self.tags = None

	@abstractmethod
	def Important_Values(self):
		pass

class Smartphone(Product):
	def __init__(self, url: str):
		super().__init__(url)
		self.category = "Smartphone"
		self.size = None

	def Important_Values(self):
		return [self.name, self.price, self.size]


class Headphone(Product):
	def __init__(self, url: str):
		super().__init__(url)
		self.category = "Headphone"
		self.noise_canceling = None

	def Important_Values(self):
		return [self.name, self.price, self.noise_canceling]


class TV(Product):
	def __init__(self, url: str):
		super().__init__(url)
		self.category = "TV"
		self.size = None

	def Important_Values(self):
		return [self.name, self.price, self.size]


class Computer(Product):
	def __init__(self, url: str):
		super().__init__(url)
		self.category = "Computer"
		self.ram = None

	def Important_Values(self):
		return [self.name, self.price, self.ram]

""" Scrape and Import File Options """

# Import the Links to be scraped. 
def Read_Links_CSV(file: str) -> list:
	file_path = os.path.join(Path_Saving, file)

	with io.open(file_path, "r", encoding="utf-8") as file_products:
		lines = file_products.readlines()
		# lines in the document consist of consequtive links divided by ";".
		phones_links = [*lines[0].translate({ord("\n"): None}).split(";")]
		tv_links = [*lines[1].translate({ord("\n"): None}).split(";")]
		computer_links = [*lines[2].translate({ord("\n"): None}).split(";")]
		headphones_link = [*lines[3].translate({ord("\n"): None}).split(";")]
	
	return phones_links, tv_links, computer_links, headphones_link

# returns the Category of the imported product.
def Generate_Product(attr: dict) -> Product:
	if attr["category"] == "Smartphone":
		product = Smartphone(attr["url"])
	elif attr["category"] == "TV":
		product = TV(attr["url"])
	elif attr["category"] == "Computer":
		product = Computer(attr["url"])
	elif attr["category"] == "Headphone":
		product = Headphone(attr["url"])
	
	for var in vars(product):
		setattr(product, var, attr[var])
	
	return product

# convert links to Product via scraper (Product_Driver).
def Convert_Product(url: str, category: str) -> Product:
	#print(f"--> url: {url}\n")
	product = Product_Driver(category, url)
	product.Get_Data()

	attributes = vars(product) 
	attributes.pop("product_content")

	return Generate_Product(attributes)

# Create lists of products via a file containing their links.
def Create_Products(file_: str) -> list:
	phones_, tv_, computer_, headphones_ = Read_Links_CSV(file_)

	phones = [Convert_Product(link, "Smartphone") for link in phones_]
	tvs = [Convert_Product(link, "TV") for link in tv_]
	computers = [Convert_Product(link, "Computer") for link in computer_]
	headphones = [Convert_Product(link, "Headphone") for link in headphones_]

	return phones, tvs, computers, headphones

# Save the products and attributes for later use.
def Write_Products_to_CSV(file_name: str, products: list):
	path = os.path.join(Path_Saving, file_name)

	with io.open(path, "w+", encoding="utf-8") as products_file:
		for item in products:
			attributes = vars(item)

			for attr in attributes:
				products_file.write(f"{attr}|{getattr(item, attr)};")
			products_file.write("\n")

""" Read already imported Products """

# Import the products that have been saved in a file.
def Read_Product_CSV(file: str) -> list:
	path = os.path.join(Path_Saving, file)
	prod_list = []

	with io.open(path, "r", encoding="utf-8") as products:
		lines = products.readlines()
		for line in lines:
			# removing ;\n from the end of the string
			cache = line[0: len(line) - 2]
			# converting str to dict
			cache = [tuple(attr.split("|")) for attr in cache.split(";")]
			prod_list.append(Generate_Product(dict(cache)))
	
	return prod_list


if __name__ == "__main__":
	start = time.perf_counter()
	test_file_links = "Links_.csv"
	test_file_products = "Products.csv"

	# testing Read_Links_CSV
	#phone, tv, computer, headphones = Read_Links_CSV(test_file_links)
	#print(f"Test Links:\nPhones: {phone}\nTV: {tv}\nComputer: {computer}\nHeadphones: {headphones}\n")
	# testing Create_Products
	#phone, tv, computer, headphone = Create_Products(test_file_links)
	#print(f"test: {type(phone[0])}, {type(tv[0])}, {type(computer[0])}, {type(headphone[0])}")
	#test_write_csv = [*phone, *tv, *computer, *headphone]
	# test Write_Products_to_CSV
	#Write_Products_to_CSV("Products.csv", test_write_csv)
	#test_read_products = Read_Product_CSV(test_file_products)
	#print(len(test_read_products))
	#for item in test_read_products:
	#	print(vars(item), "\n")

	print(f"Done in {time.perf_counter() - start} sec.")