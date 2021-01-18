import sqlite3
import random


class Supplier:
    def list_suppliers(self):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT Id, CompanyName FROM Supplier')
        info_supplier = cursor.fetchall()
        return info_supplier

    def get_supplierName(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT companyname FROM Supplier LEFT JOIN Product ON Supplier.id = Product.supplierid WHERE product.id=?', (key,))
        supplierName, = cursor.fetchall()
        return supplierName[0]

