import io, os, sys, codecs, time
import random as rd
from abc import ABC, abstractmethod

Path_Saving = "Test/"

""" Class of Persons, especially for Customers and Employees """

try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  

class Person(ABC):
	"Simple class for all the people, who you need to take track of."
	def __init__(self, name, birthday, residence, email, telephone) -> None:
		self.name = name
		self.birthday = birthday
		self.residence = residence
		self.email = email
		self.telephone = telephone
		self.last_order = None

	def Name(self) -> str:
		return self.name

	def Birthday(self) -> str:
		return self.birthday

	def Residence(self) -> str:
		return self.residence

	def Email(self) -> str:
		return self.email

	def Telephone(self) -> str:
		return self.telephone 

	def Last_Order(self):
		return self.last_order

	# Generall infos about that person.
	@abstractmethod
	def Infos(self):
		pass

	@abstractmethod
	# Assiged Customer or Employee ID. 
	def Person_ID(self):
		pass

class Customer(Person):
	"Someone, who is just a custumer to the company"
	def __init__(self, name: str = None, birthday: str = None, residence: str = None, email: str = None, telephone: int = None):
		super().__init__(name, birthday, residence, email, telephone)
		self.customer_id = hash(name)
		self.mean_volume: int = 0
		self.mean_order: int = 0
		self.mean_items: int = 0

	def Person_ID(self) -> int:
		return self.customer_id

	def Infos(self) -> list:
		return [self.name, self.customer_id, self.email, self.telephone]

class Employee(Person):
	"Employee of the company."
	def __init__(self, name: str, birthday: str = None, residence: str = None, discount :float = 0, position: str = None, email: str = None,  telephone: int = 0, employed_since: str = None):
		super().__init__(name, birthday, residence, email, telephone)
		self.employee_id = hash(name)
		self.discount = discount
		self.position = position
		self.employed_since = employed_since

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


def Read_CSV(file: str) -> list:
	file_path = os.path.join(Path_Saving, file)

	with io.open(file_path, "r", encoding="utf-8") as file_names:
		lines = file_names.readlines()
		# creating lists of the csv lines (first and last names, cities and mail provider).
		first_names = [*lines[0].translate({ord("\n"): None}).split(";")]
		last_names = [*lines[1].translate({ord("\n"): None}).split(";")]
		cities = [*lines[2].translate({ord("\n"): None}).split(";")]
		mail = [*lines[3].translate({ord("\n"): None}).split(";")]
	
	return first_names, last_names, cities, mail

def Create_Customer(first_: list, last_: list, cities: list, mails: list) -> Customer:
	name = f"{rd.choice(first_)} {rd.choice(last_)}"
	city = rd.choice(cities)
	# format: dd.mm.yyyy
	birthday = f"{rd.randint(1,31)}.{rd.randint(1,12)}.{rd.randint(1960,2005)}"
	# country code and random phone number.
	phone = f"+{rd.randint(1,60)} {rd.randint(1000000, 99999999)}"
	# spliting name into first and last for mail adress.
	cache = name.split(" ")
	# using first letter of the first name and the last name all in lower case.
	mail = f"{cache[0][0].lower()}.{cache[1].lower()}@{rd.choice(mails)}"
	return Customer(name, birthday, city, mail, phone)

def Randomize_Names(file: str, set_size: int) -> list:
	# get list of variables.
	first_names, last_names, cities, mails = Read_CSV(file)
	return [Create_Customer(first_names, last_names, cities, mails) for i in range(0, set_size)]

if __name__ == "__main__":
	start = time.perf_counter()
	# enter your file name and number of test customers.
	test_names = "Person.csv"
	set_size = 150

	# testing Read_CSV
	first_, last_, cities, mail = Read_CSV(test_names)
	print(f"Testing Read_CSV:\nfirst names: {first_}\nlast names: {last_}\ncities: {cities}\nmail: {mail}\n")
	
	# Testing Randomize_Names and Create_Customer.
	random_names = Randomize_Names(test_names, set_size)
	print(f"Testing Randomize_Names:\n")
	for customer in random_names:
		print(f"{customer.birthday}\t\t{customer.telephone}\t\t{customer.name}\t\t{customer.email}\t\t{customer.customer_id} ")
	
	print(f"Done generating {set_size} in {time.perf_counter() - start} sec.")