import os, io, sys, codecs, time
import numpy as np
import random as rd
from Personen_abc import Person, Randomize_Names
from Produktklassen_abc import Product, Read_Product_CSV

Path_Saving = "Test/"
try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  

""" Class """

class Order():
    "Create and edit an order"
    def __init__(self, person: Person, order_number: int = None, print_bag: bool = False):
        self.bag = []
        self.total = 0
        self.person = person 
        self.order_id = order_number
        self.print = print_bag

    def Show_Customer(self):
        if self.print: print(f"Current bag belongs to {self.person.name}\n")
        return self.person

    def Show_Bag(self, print_: bool = False):
        if self.print or print_:
            print(f"The current bag in total: {self.total}")
            for item_buy in self.bag:
                print(item_buy)
        return self.bag

    def Show_Order_ID(self, print_: bool = False):
        if self.print or print_: print(f"Current order ID: {self.order_id}\n")
        return self.order_id

    def Add_Product(self, product: Product, quantity: int):
        # calculate the price.
        total_price = np.around(float(product.price) * quantity, decimals=2)
        self.total += total_price

        self.bag.append([total_price, product.price, quantity, product.hash])
        if self.print: print(f"{quantity} of {product.name} for {total_price} was added to {self.person.name}`s bag.")

    def Remove_Product(self, product: Product):
        for item in self.bag:
            if item[3] == product.hash:
                remove_item = item
                break
        
        self.total -= remove_item[0]
        self.bag.remove(remove_item)

        if self.print: 
            print(f"{product.name} was removed from {self.person.name}`s bag.")

    def Show_Total(self):
        if self.print: print(f"The current bill is {np.around(self.total, decimals = 2)}")
        return np.around(self.total, decimals = 2)

    def Close_Order(self, file_name: str = None):
        path = os.path.join(Path_Saving, file_name)
        if self.print: print(f"{self.person.name}`s Order is now being processed and saved.\n Order:\n{self.bag}")
        
        if self.person != None: 
            self.person.last_order = self.order_id
        if file_name == None: 
            file_name = f"{self.order_id}_Order"

        with io.open(path, "w+", encoding="utf-8") as order_file:
            for item in self.bag:
                order_file.write(f"{item[0]};{item[1]};{item[2]};{item[3]}\n")
            order_file.close()



if __name__ == "__main__":
    start = time.perf_counter()
    test_names = "Person.csv"
    test_file_products = "Products.csv"
    test_order_save = "Order.csv"

    test_name = Randomize_Names(test_names, 1)
    test_products = Read_Product_CSV(test_file_products)

    test_order = Order(test_name[0], rd.randint(100, 1000))
    test_products = rd.sample(test_products, rd.randint(1, len(test_products) - 1))
    for item in test_products:
        print("->", item.name, item.price, "\n")

    print("----------------------------------\n")
    test_order.Show_Order_ID()
    test_order.Show_Customer()

    for item in test_products:
        test_order.Add_Product(item, rd.randint(1,3))
    
    test_order.Show_Bag(True)

    if bool(rd.choice([True, False])):
        # choose random product from list of added ones.
        delete_product = rd.sample(test_products, 1)[0]
        test_order.Remove_Product(delete_product)

    test_order.Close_Order(test_order_save)
    
    print(f"Done in {time.perf_counter() - start} sec.")