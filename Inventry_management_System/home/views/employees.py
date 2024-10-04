
from django.shortcuts import render, redirect
from home.models import Employee
from home.forms import Employee_form
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.http import JsonResponse

@login_required
@permission_required('home.view_gatepass', login_url='/login/')
def employees(request):

    employees=Employee.objects.filter(is_deleted=False)
    data={'employees':employees}
    return render(request,"employee/employee_home.html",data)   

@login_required
@permission_required('add.view_gatepass', login_url='/login/')
def add_employee(request):

    if request.method == 'POST':
        mydata=Employee.objects.filter(is_deleted=False)
        form = Employee_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee Added successfully !!")
            return redirect('addemployee')
    else:
        mydata=Employee.objects.filter(is_deleted=False)
        form = Employee_form()
    data={'form': form, 'mydata':mydata}
    return render(request, 'employee/add_employee.html', data)

@login_required
@permission_required('home.add_gatepass', login_url='/login/')
def edit_employee(request,id):

    data={}
    if request.method == 'POST':
        mydata=Employee.objects.get(id=id)
        form = Employee_form(request.POST,instance=mydata)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee Updated successfully !!")
            return redirect('addemployee')
    else:
        mydata=Employee.objects.get(id=id)
        form = Employee_form(instance=mydata)

    data={'form': form, 'mydata':mydata,'update':True}
    return render(request, 'employee/add_employee.html', data)

@login_required
@permission_required('home.delete_gatepass', login_url='/login/')
def delete_employee(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        mydata=Employee.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        return JsonResponse({'success': True, 'message': 'Employee deleted successfully!'})
    else:
        mydata=Employee.objects.get(id=id)
        mydata.is_deleted=True
        mydata.contact=""
        mydata.save()
        messages.success(request,"Employee Deleted successfully !!")
        return redirect('addemployee')
