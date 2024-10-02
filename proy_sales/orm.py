from datetime import date,datetime
from decimal import Decimal,ROUND_HALF_UP
import random
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os
import django
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Avg, Max, Min, Count
from django.db.models.functions import Substr
from argparse import Namespace
# Establece la configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_sales.settings')
# Inicializa Django
django.setup()
from django.contrib.auth.models import User
from core.models import Brand, Supplier, Product, Category, Customer, PaymentMethod, Invoice, InvoiceDetail

def probar_orm():
  def create_user(create=False):  
    for field in User._meta.fields:
      print(field.name)
    if create:  # Comprueba si create es True
        User.objects.create_user(  
            username='Lucasxxx',  
            password='1234',  
            email='abd@example.com'  
        )
        users = User.objects.all()  # Recupera todos los usuarios de la base de datos y los almacena en la variable users

        print("Listado de Usuarios")
        print(users)
  #create_user(True)
   
  def script_brands(create=False):
      if create:
        user= User.objects.get(username='dverap')
        # brand1 = Brand.objects.create(description="Nike", user=user)
        # brand2 = Brand.objects.create(description="Arroz Flor", user=user,state=False)
        # brand3 = Brand.objects.create(description="Atun Real", user=user)
        # brand4 = Brand.objects.create(description="Azucar Valdez", user=user)
        brand5 = Brand.objects.create(description="Nest cafe", user=user)
      print("Listado de las marcas")
      brands= Brand.objects.all()
      print(brands)
      brands= Brand.active_brands.all()
      for brand in brands: print(brand,brand.state) 
  #script_brands(True)
    
  def scripts_category(create=False):
      if create:
        Category.objects.filter(description__in=('electrodomesticos','Atun')).delete()
        user= User.objects.get(id=1)
        cat = Category(description='electrodomesticos',user=user)
        cat.save()
        Category(description='Atun',user=user).save()
      print("Listado de Categorias")
      print(Category.objects.all())
  # scripts_category(True)
    
  def scripts_payment_Method(create=False):
      if create:
        PaymentMethod.objects.filter(id__gte=1).delete()
        user= User.objects.get(pk=1)
        PaymentMethod.objects.bulk_create([ 
          PaymentMethod(description="Contado",user=user), 
          PaymentMethod(description="Credito",user=user), 
          PaymentMethod(description="Tarjeta",user=user) 
        ]) 
      print("Listado de los Metodos de Pagos")
      print(PaymentMethod.objects.all())
  # scripts_payment_Method(True)   
  def scripts_customer(create=False):
      if create:
        user= User.objects.get(pk=1)
        Customer.objects.bulk_create([ 
          Customer(dni='0914192182',first_name='Daniel',last_name='Vera',address='Milagro',gender='M',date_of_birth=date(1970, 5, 10),user=user), 
          Customer(dni='0914192184',first_name='Miguel',last_name='Berrones',address='9 de Octubre',gender='M',date_of_birth=date(2017, 10, 10),user=user), 
          Customer(dni='0914192185',first_name='Yady',last_name='Bohorquez',address='Pedro Carbo',gender='F',date_of_birth=date(1975, 7, 10),user=user) 
        ]) 
      
      print("Listado de los Clientes")
      customers= Customer.objects.values('id','dni','first_name','last_name')
      customers2= Customer.objects.values_list('id','dni','first_name','last_name')
      print("normal de los Clientes")
      print(Customer.objects.all())
      print("values")
      print(customers)
      print("values_list")
      print(customers2)
      print("listado de los Client")
      print(list(customers))
     
  # scripts_customer() 
  
  def script_queryset():
       Product.objects.filter(id=13).update(state=False)
       product_all = Product.objects.all()#[object1,object2]
       product_values = Product.objects.values('id','description','price','stock','state')#[{'id':1,'description':'aceite'},{}]
       product_list = Product.objects.values_list('id','description','price','stock','state')#queryset:[(1,'aceite',2),(2,'sal',4)]
       product_filter = Product.objects.filter(state=True)#[object1,object2]
       product_manager = Product.active_products.all() #[Product:'aceite',Product:'sal']
       product_exclude = Product.active_products.filter(price = 200)#[object1,object2]
       product_exclude = Product.active_products.all().exclude(price = 200)#[object1,object2]
       product_distinct = Product.objects.values('price').distinct()#[object1,object2]
       print("Listado de objetos de Productos: all")
       print(product_all)
       print("Listado de objetos de Productos: values")
       print(product_values)
       print("Listado de objetos de Productos values_list")
       print(product_list)
       print("Listado de objetos de Productos list")
       prods_list = list(product_list)#[(1,'aceite',2),(2,'sal',4)]
       prods_id = [prod[2] for prod in prods_list]#[2,4,6,8]
       print(prods_list)
       print(prods_id,max(prods_id),sum(prods_id),random.choice(prods_id))
       print("Listado de objetos de Productos: filter")
       print(product_filter)
       print("Listado de objetos de Productos: manager")
       print(product_manager)
       print("Listado de objetos de Pro ductos: exclude")
       print(product_exclude)
  script_queryset()
  
  def script_get():
       print("Objeto Producto")
       try:
         product1 = Product.active_products.get(pk=3)
         print(product1)
       except ObjectDoesNotExist:
         print("El producto con el ID 3 no existe.")  
       try:  
         product2 = get_object_or_404(Product, pk=4)
         print(product2.id,product2.description)
       except Http404 as e:
         print("¡El producto con el ID 4 no existe!")
  def script_functions():
      # filtros  operadores relacionales
      # productos_mayor = Product.active_products.filter(stock__gt=1000) # gt: stock > 1000
      # productos_mayor_igual = Product.active_products.filter(stock__gte=1000) # stock >= 1000
      # productos_menor = Product.active_products.filter(stock__lt=1000) # stock < 1000
      # productos_menor_igual = Product.active_products.filter(stock__lte=1000) # stock <= 1000
      # productos_igual = Product.active_products.filter(stock=1000) # stock = 50
      # productos_mayor_menor = Product.active_products.filter(stock__gte=1000, stock__lte=1200).values('description','stock')# stock >=1000 y <=1200
      # productos_rango = Product.objects.filter(stock__range=(1000, 1200))
      # productos_in = Product.objects.filter(stock__in=(931, 1298))
      # # print(Product.active_products.values('description','stock','expiration_date'))
      # print("Listados de productos >=1000 y <=1200")
      # print(productos_mayor_menor)
      # print(productos_rango.values_list('description','stock'))
      # print(list(productos_in.values('description','stock')))
      # filtros funciones string o cadenas
      # productos_filtro1 = Product.objects.filter(description = 'Jamon plumrose')
      # productos_filtro1 = Product.objects.filter(description__exact='Jamon plumrose')
      # productos_filtro2 = Product.objects.filter(description__iexact='jamon plumrose')
      # productos_filtro1 = Product.objects.filter(description__contains='jamon')
      # productos_filtro2 = Product.objects.filter(description__icontains='jamon')
      # productos_filtro1 = Product.objects.filter(description__startswith='jamon')
      # productos_filtro2 = Product.objects.filter(description__istartswith='jamon')
      # productos_filtro1 = Product.objects.filter(description__endswith='plumrose')
      # productos_filtro2 = Product.objects.filter(description__iendswith='plumrose')
      # productos_filtro1 = Product.objects.filter(description__in=['Jamon plumrose','carnes'])
      # #encontrar "jamon" seguido de cualquier número de espacios y luego una palabra que comienza en minuscula
      # productos_filtro1 = Product.objects.filter(description__regex=r'jamon\s+[a-z]\w*')
      # productos_filtro2 = Product.objects.filter(description__iregex=r'jamon\s+[a-z]\w*')
      # print("Listados de productos -  strings")
      # print(productos_filtro1)
      # print(productos_filtro2)
      #filtros de fechas
      # print("Listados de productos - funciones fechas")
      # products_fecha = Product.objects.filter(expiration_date__lt=date(2024, 5, 13))# <2024-05-13
      # products_fecha = Product.objects.filter(expiration_date__year__in=(2024,2025))# 
      # products_fecha = Product.objects.filter(expiration_date__month=2)#
      # products_fecha = Product.objects.filter(expiration_date__day=13)# 
      # print(products_fecha.values('description','expiration_date'))
      # # filtros logicos objeto Q
      # print(Product.active_products.values('description','stock'))
      # products_or = Product.objects.filter(Q(price__gt=2000) | Q(stock__lt=1000)) # > or <
      # products_and = Product.objects.filter( Q(stock__gt=1000) & Q(stock__lte=1200)) # > and <=
      # products_not = Product.objects.filter(~Q(stock__gt=1000)) # not > 1000
      products_union = Product.objects.filter((Q(stock__gt=1000) & Q(stock__lt=1200)) | Q(description__icontains='jamon'))
      #(stock > 1000 & stock <=1200) or (description='jamon')
      print(products_union.values('description','stock'))
  script_functions()    
  def script_agregate():
      results_agregate = Product.objects.filter(stock__gte=1000).aggregate(total_precio=Sum('price'),
                              promedio_precio=Avg('price'),
                              precio_maximo=Max('price'),
                              precio_minimo=Min('price'),
                              total_productos=Count('id')
                            )
      # print(results_agregate,results_agregate['total_precio'])
      result = Product.objects.filter(state=True).values('line').annotate(total_stock=Sum('stock')).order_by('line')
      print(result)
      # print(result.query)
      # products_total = Product.objects.annotate(name=Substr('description', 1, 5),total_value=F('price') * F('stock')).values('name','price','stock','total_value').order_by('description')
      # print(products_total)
  # script_agregate()
  def update_delete():
      Product.objects.filter(price__lt=3).update(price=F('price') * 1.10,state=True)
      Brand.objects.filter(description__icontains='Nike').delete()
      brand5 = Brand.objects.create(description="Adidas", user_id=1)
      print(brand5)
  update_delete()
  
probar_orm()