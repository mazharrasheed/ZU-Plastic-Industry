from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout, Submit
from django import forms
from django.forms import DateTimeInput
from django.contrib.auth import (authenticate, get_user_model,
                                 password_validation)
from django.contrib.auth.forms import (UserChangeForm, UserCreationForm,
                                       UsernameField)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Blog
# forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Category,Product,Account,Transaction,GatePassProduct,GatePass,Unit,Sales_Receipt
from .models import Customer,Sales_Receipt_Product,Suppliers,Cheque,Employee,Product_Price


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select Unit")
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_deleted=False), empty_label="Select Unit")
    class Meta:
        model = Product
        fields = ['category', 'productname','product_size','product_quantity','product_status','pro_img']
        labels={'productname':'Product Name','product_size':'Product Size',
                'product_quantity':'Product_Quantity','product_status':'Product_Status','pro_img':'Product Image'}
        
        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),
            
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['pro_img'].required = False
        self.fields['product_quantity'].required = False
        placeholders = {
            'productname': 'Enter product name',
            'product_size': 'Enter product size',
            'product_quantity': 'Enter quantity',
            
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Add 'fs-5' class to all fields' labels
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})  # Add class to widgets
            self.fields[field_name].label_tag = lambda label, tag=None, attrs=None, *args, **kwargs: f'<label class="fs-5" for="{self[field_name].id_for_label}">{label}</label>'
            
        self.fields['category'].empty_label = "Select"
        # self.fields['product_status'].choices = [('', 'Select')] + list(self.fields['product_status'].choices)

class Product_PriceForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")

    class Meta:
        model = Product_Price
        fields = ['product', 'customer', 'price']

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)  # Get the category from kwargs
        super(Product_PriceForm, self).__init__(*args, **kwargs)

        # Filter products based on the selected category
        if category:
            self.fields['product'].queryset = Product.objects.filter(category=category, is_deleted=False)

        placeholders = {
            'price': 'Enter product price here',
        }

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

class search_Product_PriceForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)  # Get the category from kwargs
        super(search_Product_PriceForm, self).__init__(*args, **kwargs)

        # Filter products based on the selected category
        if category:
            self.fields['product'].queryset = Product.objects.filter(category=category, is_deleted=False)

class GatePassForm(forms.ModelForm):

    RETURNABLE_CHOICES = (
        (True, 'Returnable'),
        (False, 'Non-returnable'),
    )

    returnable = forms.ChoiceField(choices=RETURNABLE_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = GatePass
        fields = ['returnable','vehicle', 'driver_phone_number','dispatch_for', 'name_of_site', 'person_name', 'phone_number']


class GatePassProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    driver_phone_number = forms.CharField(max_length=20 , label='Driver Phone Number')
    remarks = forms.CharField( label='Remarks',required=False)
    
    class Meta:
        model = GatePassProduct
        fields = ['product', 'quantity','driver_phone_number','remarks']

    def __init__(self, *args, **kwargs):
        self.gatepass = kwargs.pop('gatepass', None)
        super(GatePassProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        if product and self.gatepass:
            if GatePassProduct.objects.filter(gatepass=self.gatepass, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')

        return cleaned_data


class Sales_ReceiptForm(forms.ModelForm):
    customer_name = forms.ModelChoiceField(
        queryset=Customer.objects.filter(is_deleted=False),
        empty_label="Select Customer"
    )
    class Meta:
        model = Sales_Receipt
        fields = ['customer_name', 'phone_number']
    def __init__(self, *args, **kwargs):
        super(Sales_ReceiptForm, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['customer_name'].initial = self.instance.customer_name


class Sales_Receipt_ProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    # unit_price = forms.FloatField( label='Unit Price',required=False)
    
    class Meta:
        model = Sales_Receipt_Product
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Sales_Receipt_ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Sales_Receipt_Product.objects.filter(salereceipt=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')
        return cleaned_data
    

class Sales_Cash_ReceiptForm(forms.ModelForm):
    customer=forms.CharField(max_length=220 , required=True)
    phone_number=forms.CharField(max_length=12 , required=True)
    class Meta:
        model = Sales_Receipt
        fields = ['customer', 'phone_number']
    def __init__(self, *args, **kwargs):
        super(Sales_Cash_ReceiptForm, self).__init__(*args, **kwargs)
        # Check if an instance is passed
        if self.instance and self.instance.pk:
            # Set the initial value of customer_name
            self.fields['customer'].initial = self.instance.customer

class Sales_Cash_Receipt_ProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    unit_price = forms.FloatField( label='Unit Price',required=True)
    
    class Meta:
        model = Sales_Receipt_Product
        fields = ['product', 'quantity','unit_price']

    def __init__(self, *args, **kwargs):
        self.salereceipt = kwargs.pop('salereceipt', None)
        super(Sales_Cash_Receipt_ProductForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        if product and self.salereceipt:
            if Sales_Receipt_Product.objects.filter(salereceipt=self.salereceipt, product=product).exists():
                self.add_error('product', f'The product "{product}" has already been added to this gate pass.')
        return cleaned_data
    

class Sign_Up(UserCreationForm):

    username=UsernameField()
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Fieldset(
                'Sign Up',   
            ),
            Field('username','password1','password2', css_class="mb-3", css_id="custom_field_id",),
        
            Submit('submit', 'Submit', css_class='btn btn-info mt-3'), 
        )

class Add_Blog(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title','description')

class EditUserPrifoleForm(UserChangeForm):
    
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name','email',]
        labels={'email':'Email'}

class AdminUserPrifoleForm(UserChangeForm):
    
    password=None
    class Meta:
        model=User
        fields='__all__'
        labels={'email':'Email'}

class Employee_form(forms.ModelForm):
   
    class Meta:
        model = Employee
        fields = [ 'name','contact','job','adress']
        labels={'name':'Name',
                'contact':'Contact','adress':'Adress','job':'Job Name',}
        
        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(Employee_form, self).__init__(*args, **kwargs)
        placeholders = {
            
            'name': 'Enter full name',
            'contact': '0000-0000000',
            'adress':'Enter Adress here',
            'job':'Enter job name here',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

class Suppliers_form(forms.ModelForm):
   
    class Meta:
        model = Suppliers
        fields = ['coname', 'name','contact','adress','description']
        labels={'coname':'Company Name','name':'Name',
                'contact':'Contact','adress':'Adress','description':'Description',}
        
        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(Suppliers_form, self).__init__(*args, **kwargs)
        placeholders = {
            'coname': 'Enter company name',
            'name': 'Enter full name',
            'contact': '0000-0000000',
            'adress':'Enter Adress here'
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

class Customer_form(forms.ModelForm):
   
    class Meta:
        model = Customer
        fields = ['coname', 'name','contact','adress']
        labels={'coname':'Company Name','name':'Name',
                'contact':'Contact','adress':'Adress',}
    def __init__(self, *args, **kwargs):
        super(Customer_form, self).__init__(*args, **kwargs)
        placeholders = {
            'coname': 'Enter first name',
            'name': 'Enter full name',
            'contact': '0000-0000000',
            'adress':'Enter Adress here'
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

class Cheques_form(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.filter(is_deleted=False), empty_label="Select Customer")
    class Meta:
        model = Cheque
        fields = ['customer', 'cheque_number','cheque_amount','cheque_date','bank_name']
        labels={'customer':'Customer Name','cheuqe_Number':'Cheque Number','cheque_date':'Cheque Date','bank_name':'Bank Name/Party Name'
             }
        widgets = {
            'cheque_date': forms.DateInput(attrs={'type': 'date'}),
        }
  
    def __init__(self, *args, **kwargs):
        super(Cheques_form, self).__init__(*args, **kwargs)
        self.fields['cheque_number'].required = False
        self.fields['bank_name'].required = False
        placeholders = {
            'cheque_number': 'Enter cheque number',
            'bank_name':'Enter bank name',
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})
            
      
    

class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['name','account_type']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['name'].required = True

class Employee_AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['employee','account_type']

    def __init__(self, *args, **kwargs):
        super(Employee_AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['employee'].empty_label = "Select"
        self.fields['employee'].required = True

class Customer_AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['customer','account_type']

    def __init__(self, *args, **kwargs):
        super(Customer_AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['customer'].empty_label = "Select"
        self.fields['customer'].required = True

class Supplier_AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['supplier','account_type']

    def __init__(self, *args, **kwargs):
        super(Supplier_AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['supplier'].empty_label = "Select"
        self.fields['supplier'].required = True



class Cheque_AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['cheque','balance','account_type']

    def __init__(self, *args, **kwargs):
        super(Cheque_AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        self.fields['cheque'].empty_label = "Select"
        self.fields['cheque'].required = True
        

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'debit_account','credit_account','amount']
    
    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['debit_account'].empty_label = "Select"
        self.fields['credit_account'].empty_label = "Select"
        self.fields['debit_account'].queryset = Account.objects.filter(is_deleted=False)
        self.fields['credit_account'].queryset = Account.objects.filter(is_deleted=False)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

  