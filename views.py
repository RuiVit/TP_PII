'''
#$# Grupo 1 > 8190479 / 8190448 / 8190460 < #$#
'''
from django.template import loader, Template, Context, RequestContext
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponseNotFound
import sqlite3
from django.shortcuts import redirect,HttpResponse,render
from django import forms
from django.forms import ModelForm

# Importacao das classes criadas
from polls.product import Product
from polls.supplier import Supplier

class NameForm(forms.Form):
    product = forms.CharField(label='Product', max_length=100)
    supplier = forms.CharField(label='Supplier', max_length=100)
    unit_price = forms.DecimalField(label='UnitPrice', decimal_places=2) 
    units_in_stock = forms.IntegerField(label='UnitsInStock')  


def index(request):
    # inicializacao da classe Product na variavel product 
    product = Product()
    
    # listagem dos detalhes dos produtos
    productDetails = product.list_product()

    #do not change the lines bellow
    t = get_template('index.html')
    html = t.render({'suppliers': productDetails}) 
    return HttpResponse(html)



def read(request, key): #DONE
    product = Product()

    # obter o nome do produto, preco por unidade, unidades em stock
    # de certo produto, nomeadamente
    productName = product.get_productName(key)
    unitPrice = product.get_product_unitPrice(key) 
    unitsInStock = product.get_product_unitsInStock(key)
    
    # inicializacao da classe Supplier na variavel suppliers
    suppliers = Supplier()
    
    # obter o nome do fornecedor associado ao produto selecionado
    supplierName = suppliers.get_supplierName(key)

    # caso o stock seja 0, de modo a alertar no website
    if str(unitsInStock) == "0":
        stock_at_0 = True
    else:
        stock_at_0 = False

    #do not change the lines bellow
    # adicionada a variavel stock_at_0
    t = get_template('read.html')
    html = t.render({'id':key,'name':productName,'supplier':supplierName, \
    'unit_price':unitPrice, 'units_in_stock':unitsInStock, 'stock_at_0':stock_at_0}) 
    return HttpResponse(html)



def create(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            product = Product()
            
            # variaveis de formulario do django
            productN = form.cleaned_data['product']
            supplierN = form.cleaned_data['supplier']
            unit_price = form.cleaned_data['unit_price']
            units_in_stock = form.cleaned_data['units_in_stock']

            # criacao do produto com as informacoes obtidas anteriormente
            product.create_product(productN, supplierN, unit_price, units_in_stock)
        
        # caso "form.is_invalid" avisar com o pop-up
        else:
            return render(request, 'create.html', {'invalid_form': True})

        #do not change the line bellow
        return redirect('index')
    
    # listar todos os fornecedores disponiveis (ao criar o produto)
    suppliers = Supplier()
    allSuppliers = suppliers.list_suppliers()

    #do not change the line bellow
    return render(request, 'create.html', {'suppliers': allSuppliers})



def delete(request, key, template_name='delete.html'):
    product = Product()

    if request.method=='POST':
        # remover certo produto 
        product.delete_product(key)

        #do not change the line bellow
        return redirect('index')

    #do not change the line bellow
    name = product.get_productName(key)
    return render(request, template_name, {'productName': name})



def update(request, key, template_name='update.html'): 
    product = Product()
    suppliers = Supplier()

    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            productName = form.cleaned_data['product']
            supplierName = form.cleaned_data['supplier']
            unit_price = form.cleaned_data['unit_price']
            units_in_stock = form.cleaned_data['units_in_stock']
            
            # atualizar o produto, com as informacoes obtidas previamente
            product.update_product(productName, supplierName, unit_price, units_in_stock, key)

            #do not change the line bellow
            return redirect('index') 

        # pop-up caso algum formulario tenha um tipo errado de variavel
        else:
            return render(request, template_name, {'invalid_form': True})

    # obter o nome do produto e do fornecedor, nomeadamente
    productName = product.get_productName(key)
    supplierName = suppliers.get_supplierName(key)

    # obter a lista de fornecedores a alterar
    allSuppliers = suppliers.list_suppliers()
    
    # obter o preco por unidade e unidades em stock do produto, nomeadamente
    unitPrice = product.get_product_unitPrice(key)
    unitsInStock = product.get_product_unitsInStock(key)
    
    #do not change the line bellow
    return render(request, template_name, {'supplierName': supplierName, 
    'id':key,'productName': productName,'suppliers': allSuppliers,'unit_price':unitPrice, 'units_in_stock':unitsInStock})
    


def statistics(request, key): #DONE   
    tax = 23

    products = Product()
    
    productName = products.get_productName(key)

    # obter o total sem taxas do respetivo produto
    totalWithoutTaxes = products.get_total_without_taxes(key)

    # obter o total COM taxas do respetivo produto
    totalWithTaxes = products.get_total_including_taxes(key, tax)

    # obter a quantidade total (de acordo com as entregas) de um respetivo produto
    totalQuantity = products.get_total_quantity(key)

    # caso o stock seja zero, apresentar aviso no website
    unitsInStock = products.get_product_unitsInStock(key)
    if str(unitsInStock) == "0":
        stock_at_0 = True
    else:
        stock_at_0 = False
    
    #do not change the lines bellow
    # adicionada a variavel stock_at_0
    t = get_template('statistics.html')
    html = t.render({'name':productName, 'total_without_taxes':totalWithoutTaxes, \
    'total_with_taxes':totalWithTaxes, 'total_quantity':totalQuantity, 'tax':tax, 'stock_at_0':stock_at_0}) 
    return HttpResponse(html)

