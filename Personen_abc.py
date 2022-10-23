from numpy import str_
from Produktklassen_abc import main as main_product 
from abc import ABC, abstractmethod

"""
Code that creates a class for people. Requiered attributes are as followed: 
Name: str, Customer_ID: int, Sale: float in [0,1], Email: str,
Telephone: int with S.N. in front, i.e. (+)49, 
"""

class Person(ABC):
	"Simple class for all the people, who you need to take track of."
	Dictonary = {}

	# Name of the person. 
	def Name(self):
		return self.name

	# Date of birth
	def Birthday(self):
		return self.birthday

	# Street/no. and city of residency
	def Residence(self):
		return self.residence

	# Email adress
	def Email(self):
		return self.email

	# Mobil number. 
	def Telephone(self):
		return self.telephone 

	# Generall infos about that person.
	@abstractmethod
	def Infos(self):
		pass

	@abstractmethod
	# Assiged Customer or Employee ID. 
	def Person_ID(self):
		pass

	@abstractmethod
	def Discount(self):
		pass

	def Last_Order(self):
		return self.last_order

class Customer(Person):
	"Someone, who is just a custumer to the company"
	Dictonary = {}

	def __init__(self, name: str = None, birthday: str = None, residence: str = None, customer_id: int = None, email: str = None, telephone: int = None):
		self.name = name
		self.birthday = birthday
		self.residence = residence
		self.customer_id = customer_id
		self.email = email
		self.telephone = telephone
		self.last_order = None
		self.favourite_item = None
		self.discount_seeker = False
		self.trend_seeker = False
		self.mean_volume = None
		self.mean_order = None
		self.mean_items = None

	def Person_ID(self) -> int:
		return self.customer_id

	def Discount(self):
		return None

	def Infos(self) -> list:
		return [self.name, self.customer_id, self.email, self.telephone]

class Employee(Person):
	"Employee of the company."
	Dictonary = {"L_J_001": None, "Y_C_002": None, "M_S_003": None, }

	def __init__(self, name: str, birthday: str = None, residence: str = None, employee_id: int = 0, discount :float = 0, position: str = None, email: str = None,  telephone: int = 0, employed_since: str = None):
		self.name = name
		self.birthday = birthday
		self.residence = residence
		self.employee_id = employee_id
		self.discount = discount
		self.position = position
		self.email = email
		self.telephone = telephone
		self.employed_since = employed_since
		self.last_order = None

	def Person_ID(self) -> int:
		return self.employee_id

	def Discount(self) -> float:
		return self.discount

	def Infos(self) -> list:
		return [self.name, self.employee_id, self.email, self.telephone, self.discount]

	def Position(self) -> str:
		return self.position

	def Employed_Since(self) -> str:
		return self.employed_since
