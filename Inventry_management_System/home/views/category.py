
from django.shortcuts import render, redirect
from home.models import Category
from home.forms import CategoryForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required


@login_required
@permission_required('home.add_category', login_url='/login/')
def add_category(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
        categories=Category.objects.filter(is_deleted=False)
        mydata=Category.objects.filter(is_deleted=False)
        form = CategoryForm(request.POST)
        if form.is_valid():
          form.save()
          messages.success(request,"Category Added successfully !!")
          return redirect('category')
    else:
        mydata=Category.objects.filter(is_deleted=False)
        categories=Category.objects.filter(is_deleted=False)
        form = CategoryForm()
    data={'form': form, 'mydata':mydata,'categories':categories}
    return render(request, 'stock/add_category.html', data)
  else:
    return redirect('signin')
@login_required
@permission_required('home.change_category', login_url='/login/')
def edit_category(request,id):
  if request.user.is_authenticated:
    data={}
    if request.method == 'POST':
      categories=Category.objects.filter(is_deleted=False)
      mydata=Category.objects.get(id=id)
      form = CategoryForm(request.POST,instance=mydata)
      if form.is_valid():
        form.save()
        messages.success(request,"Category Updated successfully !!")
        return redirect('category')
    else:
      mydata=Category.objects.get(id=id)
      categories=Category.objects.filter(is_deleted=False)
      form = CategoryForm(instance=mydata)
  else:
    return redirect('signin')
  data={'form': form, 'mydata':mydata,'update':True ,'categories':categories}
  return render(request, 'stock/add_category.html', data)


@login_required
@permission_required('home.view_product', login_url='/login/')

def delete_category(request,id):
 
    mydata=Category.objects.get(id=id)
    mydata.is_deleted=True
    mydata.save()
    messages.success(request,"Category Deleted successfully !!")
    return redirect('category')

