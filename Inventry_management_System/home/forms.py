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
from .models import Category,Product,Account,Transaction,GatePassProduct,GatePass,Unit

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), empty_label="Select Unit")
    category = forms.ModelChoiceField(queryset=Category.objects.filter(is_deleted=False), empty_label="Select Unit")
    class Meta:
        model = Product
        fields = ['category', 'productname','product_size','product_quantity','product_weight','unit','product_status','pro_img']
        labels={'productname':'Product Name','product_size':'Product Size',
                'product_quantity':'Product_Quantity','product_status':'Product_Status','product_weight':'Product Weight','pro_img':'Product Image'}
        
        widgets = {

            # 'product_weight': forms.TextInput(attrs={'placeholder': 'Enter product weight'}),
            # 'pro_img': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            # 'product_status': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        placeholders = {
            'productname': 'Enter product name',
            'product_size': 'Enter product size',
            'product_quantity': 'Enter quantity',
            'product_weight':'Enter product weight'
        }
        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs.update({'placeholder': placeholder})
            
        self.fields['category'].empty_label = "Select"
        # self.fields['product_status'].choices = [('', 'Select')] + list(self.fields['product_status'].choices)













class GatePassForm(forms.ModelForm):

    RETURNABLE_CHOICES = (
        (True, 'Returnable'),
        (False, 'Non-returnable'),
    )

    returnable = forms.ChoiceField(choices=RETURNABLE_CHOICES, widget=forms.RadioSelect)
    class Meta:
        model = GatePass
        fields = ['returnable','vehicle', 'dispatch_for', 'name_of_site', 'person_name', 'phone_number']

class GatePassProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(is_deleted=False), empty_label="Select Product")
    quantity = forms.IntegerField(min_value=1, initial=1, label='Quantity')
    remarks = forms.CharField( label='Remarks',required=False)
    
    class Meta:
        model = GatePassProduct
        fields = ['product', 'quantity','remarks']

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

class AccountForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ['name','account_type']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        
        self.fields['account_type'].choices = [('', 'Select')] + list(self.fields['account_type'].choices)
        

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

  