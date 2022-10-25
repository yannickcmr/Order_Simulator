from abc import ABC, abstractmethod
import numpy as np

""" Code to create different kinds of products, i.e. Smartphones, Tvs, etc. """

class Product(ABC):
	"Class of the products"
	Dictonary = {}
	def __init__(self, url: str) -> None:
		self.url = url
		self.category = None
		self.name = None
		self.price = None
		self.sugg_price = None
		self.rating = None
		self.hash = None
		self.tags = None

	def Url(self) -> str:
		return self.url

	def Name(self) -> str:
		return self.name

	def Price(self) -> float:
		return self.price

	def Rating(self) -> list:
		return self.rating

	def Category(self) -> str:
		return self.category

	def Hash(self) -> int:
		return self.hash_code
	
	def Tags(self) -> list:
		return self.tags


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

if __name__ == "__main__":
	test_smartphone = Smartphone("https://www.amazon.de/MPXV3ZD-A/dp/B0BDJ61GFY/ref=sr_1_1_sspa?keywords=iphone+14+pro&qid=1666708676&qu=eyJxc2MiOiIzLjg5IiwicXNhIjoiMy41OSIsInFzcCI6IjMuMjQifQ%3D%3D&sprefix=ip%2Caps%2C119&sr=8-1-spons&psc=1")
	test_headphone = Headphone("https://www.amazon.de/NEW-QuietComfort-Cancelling-Ear-Personalised-White/dp/B0B7838HH6/ref=sr_1_1_sspa?crid=3T3UMCRZKE2VF&keywords=bose&qid=1666708721&qu=eyJxc2MiOiI2LjUwIiwicXNhIjoiNS43NSIsInFzcCI6IjUuMzUifQ%3D%3D&sprefix=bos%2Caps%2C132&sr=8-1-spons&psc=1")
	test_tv = TV("https://www.amazon.de/65UQ7006LB-Inches-Active-Smart-Model/dp/B0B4DGD1NM/ref=sr_1_1_sspa?crid=27TQBTVIYE7DQ&keywords=tv&qid=1666708740&qu=eyJxc2MiOiI4LjU1IiwicXNhIjoiOC40NCIsInFzcCI6IjcuNzIifQ%3D%3D&sprefix=tv%2Caps%2C100&sr=8-1-spons&psc=1")
	test_computer = Computer("https://www.amazon.de/-/en/Apple-MacBook-Air-chip-inch/dp/B08N5R7XXZ/ref=sr_1_4?crid=39XA1V7NDAML2&keywords=mac&qid=1666708761&qu=eyJxc2MiOiI1LjM3IiwicXNhIjoiNS42NyIsInFzcCI6IjUuMzEifQ%3D%3D&sprefix=mac%2Caps%2C109&sr=8-4")
