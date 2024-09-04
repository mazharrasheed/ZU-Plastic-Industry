
from django.shortcuts import render, redirect
from home.models import Customer
from home.forms import ProductForm,Customer_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def customer(request):

    customers=Customer.objects.filter(is_deleted=False)
    data={'customers':customers}
    return render(request,"customers/customers_home.html",data)   

@login_required
def add_customer(request):
 
    if request.method == 'POST':
        mydata=Customer.objects.filter(is_deleted=False)
        form = Customer_form(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Customer Added successfully !!")
          return redirect('addcustomer')
    else:
        mydata=Customer.objects.filter(is_deleted=False)
        form = Customer_form()
    data={'form': form, 'mydata':mydata}
    return render(request, 'customers/add_customer.html', data)


def edit_customer(request,id):

    data={}
    if request.method == 'POST':
      mydata=Customer.objects.get(id=id)
      form = Customer_form(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Customer Updated successfully !!")
        return redirect('addcustomer')
    else:
      mydata=Customer.objects.get(id=id)
      form = Customer_form(instance=mydata)

    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'customers/add_customer.html', data)

@login_required
def delete_customer(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        mydata=Customer.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        return JsonResponse({'success': True, 'message': 'Customer deleted successfully!'})
    else:
        mydata=Customer.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        messages.success(request,"Customer Deleted successfully !!")
        return redirect('addcustomer')
 
