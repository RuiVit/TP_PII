import sqlite3

class Product:
    def connect(self):
        self.connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.connection.close()


    def list_product(self):
        self.connect()

        self.cursor.execute('SELECT Product.Id, Product.ProductName, Supplier.companyname FROM Product INNER JOIN Supplier ON Product.SupplierId = Supplier.Id')
        info_product = self.cursor.fetchall()

        self.disconnect()
        return info_product



    def create_product(self, nomeProduto, nomeSupplier, unitsPrice, unitsInStock):
        self.connect()

        self.cursor.execute("SELECT * fROM Product WHERE id = (SELECT MAX(id) FROM Product)")
        lastid, = self.cursor.fetchall()
        
        self.cursor.execute("INSERT INTO Product \
            VALUES (?, ?, ?, 0, 0, ?, ?, 0, 0, 0)", (int(lastid[0] + 1), nomeProduto, nomeSupplier, unitsPrice, unitsInStock))
        self.connection.commit()
        self.disconnect()



    def delete_product(self, key): 
        self.connect()

        self.cursor.execute("DELETE FROM Product WHERE Id=?", (key,))
        self.connection.commit()
        self.disconnect()



    def update_product(self, productName, supplierName, unit_price, units_in_stock, key): #DONE
        self.connect()

        self.cursor.execute("UPDATE Product SET ProductName=?, SupplierId=?, UnitPrice=?, UnitsInStock=? WHERE Id=?", \
         (productName, supplierName, unit_price, units_in_stock, key))
        self.connection.commit()
        self.disconnect()   



    def get_productName(self, key):
        self.connect()

        self.cursor.execute('SELECT ProductName FROM Product WHERE Id=?', (key,))
        productName, = self.cursor.fetchall()

        self.disconnect()
        return productName[0]



    def get_product_unitPrice(self, key):
        self.connect()

        self.cursor.execute('SELECT UnitPrice FROM Product WHERE Id=?', (key,))
        unitPrice, = self.cursor.fetchall()

        self.disconnect()
        return unitPrice[0]



    def get_product_unitsInStock(self, key):
        self.connect()

        self.cursor.execute('SELECT UnitsInStock FROM Product WHERE Id=?', (key,))
        unitsInStock, = self.cursor.fetchall()

        self.disconnect()
        return unitsInStock[0]



    def get_total_without_taxes(self, key):
        self.connect()

        self.cursor.execute('SELECT UnitPrice FROM Product WHERE Id=?', (key,))
        unitPrice, = self.cursor.fetchall()
        
        self.cursor.execute('SELECT UnitsInStock FROM Product WHERE Id=?', (key,))
        unitsInStock, = self.cursor.fetchall()
    
        total = float(unitPrice[0]) * float(unitsInStock[0])
        
        self.disconnect()
        return total



    def get_total_including_taxes(self, key, tax):
        self.connect()

        total = (self.get_total_without_taxes(key) * (1 + tax / 100))

        self.disconnect()
        return total



    def get_total_quantity(self, key):
        self.connect()

        self.cursor.execute('SELECT SUM(quantity) FROM OrderDetail WHERE productid=?', (key,))
        quantity, = self.cursor.fetchall()

        self.disconnect()
        return quantity[0]
        