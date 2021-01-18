import sqlite3

class Supplier:
    def connect(self):
        self.connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()



    def list_suppliers(self):
        self.connect()

        self.cursor.execute('SELECT Id, CompanyName FROM Supplier')
        info_supplier = self.cursor.fetchall()
        
        self.disconnect()
        return info_supplier



    def get_supplierName(self, key):
        self.connect()

        self.cursor.execute('SELECT companyname FROM Supplier LEFT JOIN Product ON Supplier.id = Product.supplierid WHERE product.id=?', (key,))
        supplierName, = self.cursor.fetchall()
        
        self.disconnect()
        return supplierName[0]

