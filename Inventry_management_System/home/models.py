from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from autoslug import AutoSlugField
# Create your models here.

class Blog(models.Model):

    title=models.CharField(max_length=100)
    description=models.CharField(max_length=300)
    user=models.ForeignKey(User,on_delete=models.RESTRICT)

# models.py

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_deleted=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):

    ACTIVE = 'Atcive'
    INACTIVE = 'Inactive'

    STATUS_TYPE_CHOICES = [
        (ACTIVE , 'Active'),
        (INACTIVE ,'Inactive'),
    ]

    category=models.ForeignKey(Category,on_delete=models.RESTRICT)
    productname=models.CharField(max_length=255)
    product_size=models.CharField(max_length=255,default="")
    # product_sale_price=models.CharField(max_length=255)
    product_quantity=models.CharField(max_length=255)
    unit=models.ForeignKey(Unit , on_delete=models.RESTRICT )
    product_weight=models.CharField(max_length=255)
    # product_status=models.CharField(max_length=50,choices=STATUS_TYPE_CHOICES)
    product_status=models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    pro_img=models.ImageField(upload_to="uploaded/products/",null=True)
    product_slug=AutoSlugField(populate_from="productname",unique=True,null=True,default=None)
    def __str__(self):
        return f"{self.productname}"
    
# class GatePass(models.Model):
#     products = models.ManyToManyField(Product, through='GatePassProduct')
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Gate Pass {self.id} - {self.date_created.strftime('%Y-%m-%d')}"
    
class GatePass(models.Model):
    products = models.ManyToManyField(Product, through='GatePassProduct')
    date_created = models.DateTimeField(auto_now_add=True)
    vehicle = models.CharField(max_length=255)
    driver_phone_number = models.CharField(max_length=20)
    dispatch_for = models.CharField(max_length=255)
    name_of_site = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    returnable=models.BooleanField(null=True)
    # prepared_by=models.CharField(max_length=255,default='')
    # authorized_by=models.CharField(max_length=255,default='')

    def __str__(self):
        return f"Gate Pass {self.id} - {self.date_created.strftime('%Y-%m-%d')}"
    
class GatePassProduct(models.Model):
    gatepass = models.ForeignKey(GatePass, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    remarks=models.CharField(max_length=255,null=True)
    
    def __str__(self):
        return f"{self.product.productname} (Qty: {self.quantity})"
    
    
class Sales_Reciept(models.Model):
    products = models.ManyToManyField(Product, through='Sales_Reciept_Product')
    date_created = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT,null=True)

    def __str__(self):
        return f"Sale Reciept {self.id} - {self.date_created.strftime('%Y-%m-%d')}"
     
class Sales_Reciept_Product(models.Model):
    salereceipt = models.ForeignKey(Sales_Reciept, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField()
    unit_price = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.product.productname} (Qty: {self.quantity})"
    
class Suppliers(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    adress=models.CharField(max_length=255)
    contact=models.CharField(max_length=12,null=True,unique=True)
    description=models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
class Customer(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    adress=models.CharField(max_length=255)
    contact=models.CharField(max_length=12,null=True,unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    

class Cheque(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.RESTRICT)
    cheque_number=models.CharField(max_length=20,null=True)
    cheque_date=models.DateField()
    bank_name=models.CharField(max_length=50,null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} {self.cheque_number}"
    

class Account(models.Model):
    ASSET = 'Asset'
    LIABILITY = 'Liability'
    EQUITY = 'Equity'
    REVENUE = 'Revenue'
    EXPENSE = 'Expense'
    GAIN = 'Gain'
    LOSS = 'Loss'

    ACCOUNT_TYPE_CHOICES = [
        (ASSET, 'Asset'),
        (LIABILITY, 'Liability'),
        (EQUITY, 'Equity'),
        (REVENUE, 'Revenue'),
        (EXPENSE, 'Expense'),
        (GAIN, 'Gain'),
        (LOSS, 'Loss'),
    ]

    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return self.name
    


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    debit_account = models.ForeignKey(Account, related_name='debit_transactions', on_delete=models.RESTRICT)
    credit_account = models.ForeignKey(Account, related_name='credit_transactions', on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date} - {self.description}"