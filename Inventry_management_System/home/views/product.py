
from django.shortcuts import render, redirect
from home.models import Product,Category
from home.forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def products(request):
    categories=Category.objects.filter(is_deleted=False)
    categoryID=(request.GET.get('category'))
    if categoryID:
        products=Product.objects.filter(category=categoryID,is_deleted=False)
        # products=Product.objects.filter(is_deleted=False)
        print(products)
    else:
        products=Product.objects.filter(is_deleted=False).order_by('category')
    data={'products':products,'categories':categories}
    return render(request,"stock/products_home.html",data)   

@login_required
def add_product(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        mydata=Product.objects.filter(is_deleted=False)
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
          form.save()
          messages.success(request,"Product Added successfully !!")
          return redirect('product')
    else:
        mydata=Product.objects.filter(is_deleted=False)
        form = ProductForm()
    data={'form': form, 'mydata':mydata}
    return render(request, 'stock/add_Product.html', data)
  else:
    return redirect('signin')

def edit_product(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Product.objects.get(id=id)
      form = ProductForm(request.POST,request.FILES,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Product Updated successfully !!")
        return redirect('product')
    else:
      mydata=Product.objects.get(id=id)
      form = ProductForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True}
  return render(request, 'stock/add_Product.html', data)

@login_required
def delete_product(request,id):
 
  if request.user.is_authenticated:

    mydata=Product.objects.get(id=id)
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Product Deleted successfully !!")
    return redirect('product')

  else:

    return redirect('signin')
 
