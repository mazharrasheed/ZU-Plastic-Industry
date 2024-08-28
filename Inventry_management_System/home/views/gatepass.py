# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  GatePassProductForm,GatePassForm
from ..models import GatePass, GatePassProduct,Product
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def gatepass(request):
    form = GatePassProductForm()
    form_gatepass=GatePassForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass':form_gatepass,   
    })

@login_required
def create_gatepass(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = GatePass.objects.create()
        return redirect('create_gatepass', gatepass_id=gatepass.id)

    if request.method == 'POST':
        form = GatePassProductForm(request.POST, gatepass=gatepass)
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
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = GatePassProductForm(gatepass=gatepass)
        form_gatepass = GatePassForm(instance=gatepass)

    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'gatepass_products': gatepass_products,
        'form_gatepass': form_gatepass,
        'gatepass': gatepass,
    })

@login_required
def edit_gatepass(request, gatepass_id=None):
    update=True
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = GatePass.objects.create()
        return redirect('create_gatepass', gatepass_id=gatepass.id)

    if request.method == 'POST':
        form = GatePassProductForm(request.POST, gatepass=gatepass)
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
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = GatePassProductForm(gatepass=gatepass)
        form_gatepass = GatePassForm(instance=gatepass)

    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    return render(request, 'gatepass/edit_gatepass.html', {
        'form': form,
        'gatepass_products': gatepass_products,
        'form_gatepass': form_gatepass,
        'gatepass': gatepass,
        'update':update
    })

@login_required
def delete_gatepass_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(GatePassProduct, id=id)
        gatepass_id = request.POST.get('gatepass_id')
        product.delete()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def cancel_gatepass(request,id):
    # gatepass_id=(request.GET.get('gatepass_id'))
    gatepass=get_object_or_404(GatePass,id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    # 
    if gatepass_products:
        for item in gatepass_products:
            item.delete()
    gatepass.delete()
    messages.success(request, "Your gatepass canceled !") 
    return redirect('list_gatepasses')

@login_required
def delete_gatepass1(request,id):
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

def delete_gatepass(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        gatepass = get_object_or_404(GatePass, id=id)
        gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
        if gatepass_products:
            gatepass_products.delete()  # Bulk delete all related products
        gatepass.delete()
        return JsonResponse({'success': True, 'message': 'Gatepass deleted successfully!'})
    
    # For non-AJAX requests, handle as usual
    gatepass = get_object_or_404(GatePass, id=id)
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
    if gatepass_products:
        gatepass_products.delete()  # Bulk delete all related products
    gatepass.delete()
    messages.success(request, "Gatepass deleted successfully!")
    return redirect('list_gatepasses')

@login_required
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

@login_required
def print_gatepass(request, gatepass_id):
    # Fetch the GatePass instance by ID
    gatepass = get_object_or_404(GatePass, id=gatepass_id)
    # Fetch all products associated with this GatePass
    gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)

    return render(request, 'gatepass/print_gatepass.html', {
        'gatepass': gatepass,
        'gatepass_products': gatepass_products,
        
    })
