
from django.shortcuts import render, redirect
from home.models import Suppliers
from home.forms import ProductForm,Suppliers_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def supplier(request):

    suppliers=Suppliers.objects.filter(is_deleted=False)
    data={'suppliers':suppliers}
    return render(request,"suppliers/suppliers_home.html",data)   

@login_required
def add_supplier(request):
 
    if request.method == 'POST':
        mydata=Suppliers.objects.filter(is_deleted=False)
        form = Suppliers_form(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Supplier Added successfully !!")
          return redirect('addsupplier')
    else:
        mydata=Suppliers.objects.filter(is_deleted=False)
        form = Suppliers_form()
    data={'form': form, 'mydata':mydata}
    return render(request, 'suppliers/add_supplier.html', data)


def edit_supplier(request,id):

    data={}
    if request.method == 'POST':
      mydata=Suppliers.objects.get(id=id)
      form = Suppliers_form(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Supplier Updated successfully !!")
        return redirect('addsupplier')
    else:
      mydata=Suppliers.objects.get(id=id)
      form = Suppliers_form(instance=mydata)

    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'suppliers/add_supplier.html', data)

@login_required
def delete_supplier(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        mydata=Suppliers.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        return JsonResponse({'success': True, 'message': 'Supplier deleted successfully!'})
    else:
        mydata=Suppliers.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        messages.success(request,"Supplier Deleted successfully !!")
        return redirect('addsupplier')
 