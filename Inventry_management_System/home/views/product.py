
from django.shortcuts import render, redirect
from home.models import Product,Category
from home.forms import ProductForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required

@login_required
@permission_required('home.view_product', login_url='/login/')
def products(request):
    category_selected=False
    categoryID=(request.GET.get('category'))
    if categoryID:
        categories=Category.objects.filter(is_deleted=False,id=categoryID)
        category_selected=True
        products=Product.objects.filter(category=categoryID,is_deleted=False)
        # products=Product.objects.filter(is_deleted=False)
        print(products)
    else:
        categories=Category.objects.filter(is_deleted=False)
        products=Product.objects.filter(is_deleted=False).order_by('category')
    data={'products':products,'categories':categories,'category_selected':category_selected}
    return render(request,"stock/products_home.html",data)   

@login_required
# @permission_required('home.add_sales_product', login_url='/login/')
def add_product(request,id=''):
  if id:
    categories=Category.objects.filter(is_deleted=False,id=id)
  else:
    categoryID=int((request.GET.get('category')))
    categories=Category.objects.filter(is_deleted=False,id=categoryID)
  if request.method == 'POST':
      mydata=Product.objects.filter(is_deleted=False)
      form = ProductForm(request.POST,request.FILES)
      if form.is_valid():
        form.save()
        messages.success(request,"Product Added successfully !!")
        if id:
          return redirect('addproduct1',id)
        else:
          return redirect('addproduct1',categoryID)
  else:
      
      if id:
        cat=Category.objects.get(is_deleted=False,id=id)
      else:
        cat=Category.objects.get(is_deleted=False,id=categoryID)

      mydata=Product.objects.filter(is_deleted=False,category=cat).order_by("-id")
      form = ProductForm(initial={'category': cat})
  data={'form': form, 'mydata':mydata,'categories':categories,'prod':True}
  return render(request, 'stock/add_Product.html', data)

@login_required
@permission_required('home.change_sales_product', login_url='/login/')
def edit_product(request,id):
  data={}
  if request.method == 'POST':
    mydata=Product.objects.get(id=id)
    form = ProductForm(request.POST,request.FILES,instance=mydata)
    if form.is_valid():
      form.save()
      messages.success(request,"Product Updated successfully !!")
      return redirect('addproduct')
  else:
    mydata=Product.objects.get(id=id) 
    form = ProductForm(instance=mydata)
  data={'form': form, 'mydata':mydata,'update':True,}
  return render(request, 'stock/add_Product.html', data)

@login_required
@permission_required('home.delete_product', login_url='/login/')
def delete_product(request,id):
  
  mydata=Product.objects.get(id=id)
  mydata.is_deleted=True
  mydata.save()
  messages.success(request,"Product Deleted successfully !!")
  return redirect('addproduct')
 
