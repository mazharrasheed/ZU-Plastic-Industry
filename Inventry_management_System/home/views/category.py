
from django.shortcuts import render, redirect
from home.models import Category
from home.forms import CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def add_category(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        mydata=Category.objects.filter(is_deleted=False)
        form = CategoryForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Category Added successfully !!")
          return redirect('category')
    else:
        mydata=Category.objects.filter(is_deleted=False)
        form = CategoryForm()
    data={'form': form, 'mydata':mydata}
    return render(request, 'stock/add_category.html', data)
  else:
    return redirect('signin')

def edit_category(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      mydata=Category.objects.get(id=id)
      form = CategoryForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Category Updated successfully !!")
        return redirect('category')
    else:
      mydata=Category.objects.get(id=id)
      form = CategoryForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True}
  return render(request, 'stock/add_category.html', data)

def delete_category(request,id):
 
  if request.user.is_authenticated:

    mydata=Category.objects.get(id=id)
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Category Deleted successfully !!")
    return redirect('category')

  else:

    return redirect('signin')
 
