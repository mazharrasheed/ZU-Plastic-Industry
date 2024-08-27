# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  GatePassProductForm,GatePassForm
from ..models import GatePass, GatePassProduct,Product
from django.contrib import messages

product_list=[]

@login_required

def gatepass(request):
   
    form = GatePassProductForm()
    form_gatepass=GatePassForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass':form_gatepass,   
    })

def create_gatepass1(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)

    else:
        gatepass = GatePass.objects.create()
        if request.method == 'POST':
            form = GatePassProductForm(request.POST)
            form_gatepass = GatePassForm(request.POST, instance=gatepass)
            if form.is_valid() and form_gatepass.is_valid():
                # Update the GatePass object with the form_gatepass data
                form_gatepass.save()  # This will update the existing instance
                
                # Save the GatePassProduct object and associate it with the updated GatePass
                gatepass_product = form.save(commit=False)
                gatepass_product.gatepass = gatepass
                gatepass_product.save()
                return redirect('create_gatepass', gatepass_id=gatepass.id)

    if request.method == 'POST':
        form = GatePassProductForm(request.POST)
        form_gatepass = GatePassForm(request.POST, instance=gatepass)
        if form.is_valid() and form_gatepass.is_valid():
            # Update the GatePass object with the form_gatepass data
            form_gatepass.save()  # This will update the existing instance
            
            # Save the GatePassProduct object and associate it with the updated GatePass
            gatepass_product = form.save(commit=False)
            gatepass_product.gatepass = gatepass
            gatepass_product.save()
            return redirect('create_gatepass', gatepass_id=gatepass.id)
    else:
        form = GatePassProductForm()
        form_gatepass=GatePassForm(instance=gatepass)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'gatepass_products': gatepass_products,
        'form_gatepass':form_gatepass,
        'gatepass': gatepass,
    })

from django.http import JsonResponse
from django.template.loader import render_to_string

def create_gatepass(request, gatepass_id=None):

    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = GatePass.objects.create()
        return redirect('create_gatepass', gatepass_id=gatepass.id)
    if request.method == 'POST':
        form = GatePassProductForm(request.POST)
        form_gatepass = GatePassForm(request.POST, instance=gatepass)
        if form.is_valid() and form_gatepass.is_valid():
            form_gatepass.save()
            gatepass_product = form.save(commit=False)
            gatepass_product.gatepass = gatepass
            gatepass_product.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
                rendered_products = render_to_string('gatepass/gatepass_product_list.html', {
                    'gatepass_products': gatepass_products,
                    'gatepass_id': gatepass.id,
                })
                return JsonResponse({
                    'success': True,
                    'rendered_products': rendered_products,
                    'gatepass_id': gatepass.id,
                })
            return redirect('create_gatepass', gatepass_id=gatepass.id)
    else:
        form = GatePassProductForm()
        form_gatepass = GatePassForm(instance=gatepass)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'gatepass_products': gatepass_products,
        'form_gatepass': form_gatepass,
        'gatepass': gatepass,
    })

def edit_gatepass(request, gatepass_id=None):
    update=True
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = GatePass.objects.create()
        if request.method == 'POST':
            form = GatePassProductForm(request.POST)
            form_gatepass = GatePassForm(request.POST, instance=gatepass)
            if form.is_valid() and form_gatepass.is_valid():
                # Update the GatePass object with the form_gatepass data
                form_gatepass.save()  # This will update the existing instance
                
                # Save the GatePassProduct object and associate it with the updated GatePass
                gatepass_product = form.save(commit=False)
                gatepass_product.gatepass = gatepass
                gatepass_product.save()
                return redirect('edit_gatepass', gatepass_id=gatepass.id)

    if request.method == 'POST':
        form = GatePassProductForm(request.POST)
        form_gatepass = GatePassForm(request.POST, instance=gatepass)
        if form.is_valid() and form_gatepass.is_valid():
            # Update the GatePass object with the form_gatepass data
            form_gatepass.save()  # This will update the existing instance
            
            # Save the GatePassProduct object and associate it with the updated GatePass
            gatepass_product = form.save(commit=False)
            gatepass_product.gatepass = gatepass
            gatepass_product.save()
            return redirect('edit_gatepass', gatepass_id=gatepass.id)
    else:
        form = GatePassProductForm()
        form_gatepass=GatePassForm(instance=gatepass)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    print(update)
    return render(request, 'gatepass/edit_gatepass.html', {
        'form': form,
        'gatepass_products': gatepass_products,
        'form_gatepass':form_gatepass,
        'gatepass': gatepass,
        'update':update
    })

def delete_gatepass_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(GatePassProduct, id=id)
        gatepass_id = request.POST.get('gatepass_id')
        product.delete()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def delete_gatepass_item1(request,id):
    print('i m delete item')
    gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=gatepass_id)
    gatepass_product = GatePassProduct.objects.get(id=id,gatepass=gatepass)
    print(gatepass_product)
    gatepass_product.delete()
    return redirect('create_gatepass', gatepass_id=gatepass_id)

def update_delete_gatepass_item(request,id):
    print('i m delete item')
    gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=gatepass_id)
    gatepass_product = GatePassProduct.objects.get(id=id,gatepass=gatepass)
    print(gatepass_product)
    gatepass_product.delete()
    return redirect('edit_gatepass', gatepass_id=gatepass_id)

def cancel_gatepass(request,id):
    # gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    # 
    if gatepass_products:
        for item in gatepass_products:
            item.delete()
    gatepass.delete()
    messages.success(request, "Your action canceled successful!") 
    return redirect('list_gatepasses')

def delete_gatepass(request,id):
    print('i m delete item')
    # gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    if gatepass_products:
        for item in gatepass_products:
            item.delete()
    gatepass.delete()
    messages.success(request, "Gatepass deleted successful!")    
    return redirect('list_gatepasses')



def list_gatepasses(request):
    gatepass_items_pro={}
    gatepasses = GatePass.objects.all()
    gatepasses
    gatepass_products = GatePassProduct.objects.all().count()
    for x in gatepasses:
        gatepass_items_pro[x.id] = GatePassProduct.objects.filter(gatepass=x).count()

    return render(request, 'gatepass/list_gatepasses.html', {
        'gatepasses': gatepasses,
        'gatepass_items_pro': gatepass_items_pro,
        })

def print_gatepass(request, gatepass_id):
    # Fetch the GatePass instance by ID
    gatepass = get_object_or_404(GatePass, id=gatepass_id)
    # Fetch all products associated with this GatePass
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)

    return render(request, 'gatepass/print_gatepass.html', {
        'gatepass': gatepass,
        'gatepass_products': gatepass_products,
        
    })
