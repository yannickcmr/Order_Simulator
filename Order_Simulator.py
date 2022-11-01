import io, os, sys, codecs, time
import random as rd
import numpy as np
from Personen_abc import Randomize_Names
from Produktklassen_abc import Read_Product_CSV
from Bestellungen import Order

Path_Saving = "Test/"
try:
    sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
except:
    pass  

def Generate_Orders(file:str, products: list, customers: list = None,  set_size: int = 100, show: bool = False):
    if customers == None:
        customers = Randomize_Names("Person.csv", set_size)
    
    order_list = []
    for i, customer in enumerate(customers):
        products_order = rd.sample(products, rd.randint(1, len(products) - 1))
        # random order id.
        order = Order(customer, int(432023 + i))
        
        for prod in products_order:
            order.Add_Product(prod, rd.randint(1,2))
        
        order_list.append(order)
    
    path = os.path.join(Path_Saving, file)
    with io.open(path, "w+", encoding="utf-8") as file_orders:
        for order in order_list:
            file_orders.write(f"{order.order_id};{order.total};{order.person.customer_id};")
            for prod in order.bag:
                # prod[x], x=1 : price, x=2 : quantity, x=3 : hash id
                file_orders.write(f"{prod[1]};{prod[2]};{prod[3]}:")
            file_orders.write("\n")
    
    return order_list

if __name__ == "__main__":
    start = time.perf_counter()
    test_file_products = "Products.csv"
    test_orders_save = "Orders.csv"

    test_products = Read_Product_CSV(test_file_products)
    Generate_Orders(test_orders_save, test_products, set_size=1000, show=True)

    print(f"Done in {time.perf_counter() - start} sec.")
