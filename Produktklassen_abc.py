from abc import ABC, abstractmethod
import numpy as np

""" Code to create different kinds of products, i.e. Smartphones, Tvs, etc. """

class Product(ABC):
	"Class of the company´s products"
	Dictonary = {}

	# Name of the product
	def Name(self):
		return self.name

	def Manufactor(self):
		return self.manufactor	

	# Price of the product.
	def Price(self):
		return float(self.price)

	# Relative Ranking compared to equivalent products
	def Ranking(self):
		return int(self.ranking)

	# Category, which it belongs to
	def Category(self):
		return self.category

	@abstractmethod
	def Important_Values(self):
		pass


class Smartphone(Product):
	def __init__(self, url: str, name: str, price: float, manufactor: str, ranking: int = 0, rating: list = None, size: int = 0):
		self.category = "Smartphone"
		self.url = url
		self.name = name
		self.manufactor = manufactor
		self.price = price
		self.ranking = ranking
		self.rating = rating
		self.size = size

	def Important_Values(self):
		return [self.name, self.manufactor, self.price, self.size]

class Headphone(Product):
	def __init__(self, url: str, name: str, price: float, manufactor: str, ranking: int = 0,rating: list = None, NC: bool = False):
		self.category = "Headphone"
		self.url = url
		self.name = name
		self.manufactor = manufactor
		self.price = price
		self.ranking = ranking
		self.rating = rating
		self.noise_canceling = NC

	def Important_Values(self):
		return [self.name, self.manufactor, self.price, self.noise_canceling]

class TV(Product):
	def __init__(self, url: str, name: str, price: float, manufactor: str, ranking: int = 0,rating: list = None, size: int = 0):
		self.category = "TV"
		self.url = url
		self.name = name
		self.manufactor = manufactor
		self.price = price
		self.ranking = ranking
		self.rating = rating
		self.size = size

	def Important_Values(self):
		return [self.name, self.manufactor, self.price, self.size]

class Computer(Product):
	def __init__(self, url: str, name: str, price: float, manufactor: str, ranking: int = 0,rating: list = None, ram: int = 4):
		self.category = "Computer"
		self.url = url
		self.name = name
		self.manufactor = manufactor
		self.price = price
		self.ranking = ranking
		self.rating = rating
		self.ram = ram


	def Important_Values(self):
		return [self.name, self.manufactor, self.price, self.ram]