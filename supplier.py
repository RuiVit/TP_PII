'''
#$# Grupo 1 > 8190479 / 8190448 / 8190460 < #$#
'''
#importar a biblioteca sqlite3, para gestao da base de dados
import sqlite3

class Supplier:
    # realizar a ligacao a base de dados
    def connect(self):
        self.connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        self.cursor = self.connection.cursor()

    # terminar a ligacao a base de dados
    def disconnect(self):
        self.connection.close()


    # listar o fornecedor
    def list_suppliers(self):
        self.connect()

        self.cursor.execute('SELECT Id, CompanyName FROM Supplier')
        info_supplier = self.cursor.fetchall()
        
        self.disconnect()
        return info_supplier


    # listar o nome do fornecedor associado a certo produto
    def get_supplierName(self, key):
        self.connect()

        self.cursor.execute('SELECT companyname FROM Supplier LEFT JOIN Product ON Supplier.id = Product.supplierid WHERE product.id=?', (key,))
        supplierName, = self.cursor.fetchall()
        
        self.disconnect()
        return supplierName[0]

