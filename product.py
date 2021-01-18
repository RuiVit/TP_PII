import sqlite3

class Product:
    def list_product(self):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT Product.Id, Product.ProductName, Supplier.companyname FROM Product INNER JOIN Supplier ON Product.SupplierId = Supplier.Id')
        info_product = cursor.fetchall()
        return info_product

    def create_product(self, nomeProduto, nomeSupplier, unitsPrice, unitsInStock):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute("SELECT * fROM Product WHERE id = (SELECT MAX(id) FROM Product)")
        lastid, = cursor.fetchall()
        
        cursor.execute("INSERT INTO Product \
            VALUES (?, ?, ?, 0, 0, ?, ?, 0, 0, 0)", (int(lastid[0] + 1), nomeProduto, nomeSupplier, unitsPrice, unitsInStock))
        connection.commit()

    def delete_product(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Product WHERE Id=?", (key,))
        connection.commit()

    def update_product(self, productName, supplierName, unit_price, units_in_stock, key): #DONE
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute("UPDATE Product SET ProductName=?, SupplierId=?, UnitPrice=?, UnitsInStock=? WHERE Id=?", (productName, supplierName, unit_price, units_in_stock, key))
        connection.commit()   

    def get_productName(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT ProductName FROM Product WHERE Id=?', (key,))
        productName, = cursor.fetchall()
        return productName[0]

    def get_product_unitPrice(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT UnitPrice FROM Product WHERE Id=?', (key,))
        unitPrice, = cursor.fetchall()
        return unitPrice[0]

    def get_product_unitsInStock(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT UnitsInStock FROM Product WHERE Id=?', (key,))
        unitsInStock, = cursor.fetchall()
        return unitsInStock[0]

    def get_total_without_taxes(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT UnitPrice FROM Product WHERE Id=?', (key,))
        unitPrice, = cursor.fetchall()
        
        cursor.execute('SELECT UnitsInStock FROM Product WHERE Id=?', (key,))
        unitsInStock, = cursor.fetchall()
    
        total = float(unitPrice[0]) * float(unitsInStock[0])
        return total

    def get_total_including_taxes(self, key, tax):
        products = Product()
        total = (products.get_total_without_taxes(key) * (1 + tax / 100))
        return total

    def get_total_quantity(self, key):
        connection = sqlite3.connect(r'C:\Users\RandomPenguin\Desktop\CRSI\PII\TPPII\db\Northwind.sqlite')
        cursor = connection.cursor()

        cursor.execute('SELECT COUNT(Productid) FROM OrderDetail WHERE productid=?', (key,))
        quantity, = cursor.fetchall()
        return quantity[0]
        