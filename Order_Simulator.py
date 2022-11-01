import io, os, sys, codecs, time
import random as rd
import numpy as np
from Personen_abc import Customer, Randomize_Names
from Produktklassen_abc import Product
from Bestellungen import Order

Path_Saving = "Test/"
try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  

def Generate_Orders(products: list, customers: list = None,  set_size: int = 100):
    if customers == None:
        customers = Randomize_Names("Person.csv")
    



if __name__ == "__main__":
    start = time.perf_counter()
    test_names = "Person.csv"
    test_file_products = "Products.csv"
    test_order_save = "Orders.csv"