from django.template import loader, Template, Context, RequestContext
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponseNotFound
import sqlite3
from django.shortcuts import redirect,HttpResponse,render
from django import forms
from django.forms import ModelForm

from polls.product import Product
from polls.supplier import Supplier

class NameForm(forms.Form):
    product = forms.CharField(label='Product', max_length=100)
    supplier = forms.CharField(label='Supplier', max_length=100)
    unit_price = forms.DecimalField(label='UnitPrice', decimal_places=2) 
    units_in_stock = forms.IntegerField(label='UnitsInStock')  

def index(request): #DONE 
    product = Product()
    
    productDetails = product.list_product()

    #do not change the lines bellow
    t = get_template('index.html')
    html = t.render({'suppliers': productDetails}) 
    return HttpResponse(html)

def read(request, key): #DONE
    product = Product()

    productName = product.get_productName(key)
    unitPrice = product.get_product_unitPrice(key) 
    unitsInStock = product.get_product_unitsInStock(key)
    
    suppliers = Supplier()
    
    supplierName = suppliers.get_supplierName(key)

    if str(unitsInStock) == "0":
        stock_at_0 = True
    else:
        stock_at_0 = False

    #do not change the lines bellow
    t = get_template('read.html')
    html = t.render({'id':key,'name':productName,'supplier':supplierName, \
    'unit_price':unitPrice, 'units_in_stock':unitsInStock, 'stock_at_0':stock_at_0}) 
    return HttpResponse(html)

def create(request): #DONE
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            product = Product()
            
            productN = form.cleaned_data['product']
            supplierN = form.cleaned_data['supplier']
            unit_price = form.cleaned_data['unit_price']
            units_in_stock = form.cleaned_data['units_in_stock']

            product.create_product(productN, supplierN, unit_price, units_in_stock)
        #do not change the line bellow
        return redirect('index')
    
    suppliers = Supplier()
    allSuppliers = suppliers.list_suppliers()

    #do not change the line bellow
    return render(request, 'create.html', {'suppliers': allSuppliers})

def delete(request, key, template_name='delete.html'): #DONE
    if request.method=='POST':
        product = Product()
        product.delete_product(key)

        #do not change the line bellow
        return redirect('index')

    #do not change the line bellow
    return render(request, template_name)

def update(request, key, template_name='update.html'): #DONE
    product = Product()
    suppliers = Supplier()

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            try:
                productName = form.cleaned_data['product']
                supplierName = form.cleaned_data['supplier']
                unit_price = form.cleaned_data['unit_price']
                units_in_stock = form.cleaned_data['units_in_stock']
            #Alguma variavel foi do tipo errado
            except KeyError:
                return render(request, template_name, {'invalid_form': True})

            product.update_product(productName, supplierName, unit_price, units_in_stock, key)

            #do not change the line bellow
            return redirect('index') 

    productName = product.get_productName(key)
    supplierName = suppliers.get_supplierName(key)

    allSuppliers = suppliers.list_suppliers()
    
    unitPrice = product.get_product_unitPrice(key)
    unitsInStock = product.get_product_unitsInStock(key)
    
    #do not change the line bellow
    return render(request, template_name, {'supplierName': supplierName, 
    'id':key,'productName': productName,'suppliers': allSuppliers,'unit_price':unitPrice, 'units_in_stock':unitsInStock})
    
def statistics(request, key): #DONE   
    tax = 23

    products = Product()
    
    productName = products.get_productName(key)

    totalWithoutTaxes = products.get_total_without_taxes(key)

    totalWithTaxes = products.get_total_including_taxes(key, tax)

    totalQuantity = products.get_total_quantity(key)

    unitsInStock = products.get_product_unitsInStock(key)
    if str(unitsInStock) == "0":
        stock_at_0 = True
    else:
        stock_at_0 = False
    
    #do not change the lines bellow
    #Foi tambem passado a variavel stock_at_0
    t = get_template('statistics.html')
    html = t.render({'name':productName, 'total_without_taxes':totalWithoutTaxes, \
    'total_with_taxes':totalWithTaxes, 'total_quantity':totalQuantity, 'tax':tax, 'stock_at_0':stock_at_0}) 
    return HttpResponse(html)

