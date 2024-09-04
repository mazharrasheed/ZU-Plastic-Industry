

# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Sales_Reciept_ProductForm,Sales_RecieptForm
from ..models import Sales_Reciept, Sales_Reciept_Product,Product
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum


@login_required
def list_sales(request):
    salereceipt_items_pro={}
    salereceipts = Sales_Reciept.objects.all()
    print(salereceipts)
    salereceipts
    gatepass_products = Sales_Reciept_Product.objects.all().count()
    for x in salereceipts:
        salereceipt_items_pro[x.id] = Sales_Reciept_Product.objects.filter(salereceipt=x).count()

    return render(request, 'sale/list_sales.html', {
        'salereceipts': salereceipts,
        'salereceipt_items_pro': salereceipt_items_pro,
        })

@login_required
def salereceipt(request):
    form = Sales_Reciept_ProductForm()
    form_salereceipt=Sales_RecieptForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_salereceipt':form_salereceipt,   
    })

@login_required
def create_salereceipt(request, salereceipt_id=None):
    if salereceipt_id:
        salereceipt = get_object_or_404(Sales_Reciept, id=salereceipt_id)
    else:
        salereceipt = Sales_Reciept.objects.create()
        return redirect('create_salereceipt', salereceipt_id=salereceipt.id)

    if request.method == 'POST':
        form = Sales_Reciept_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Sales_RecieptForm(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            unit_price = form.cleaned_data.get('unit_price')
            qty = form.cleaned_data.get('quantity')
            amount=unit_price*qty
            salereceipt_product = form.save(commit=False)
            salereceipt_product.salereceipt = salereceipt
            salereceipt_product.amount = amount
            salereceipt_product.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
                rendered_products = render_to_string('sale/salereceipt_product_list.html', {
                    'salereceipt_products': salereceipt_products,
                    'salereceipt_id': salereceipt.id,
                })
                return JsonResponse({
                    'success': True,
                    'rendered_products': rendered_products,
                    'salereceipt_id': salereceipt.id,
                })
            return redirect('create_salereceipt', salereceipt_id=salereceipt.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Sales_Reciept_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Sales_RecieptForm(instance=salereceipt)

    salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
    return render(request, 'sale/create_salereceipt.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
    })

@login_required
def edit_salereceipt(request, salereceipt_id=None):
    update=True
    if salereceipt_id:
        salereceipt = get_object_or_404(Sales_Reciept, id=salereceipt_id)
    else:
        salereceipt = Sales_Reciept.objects.create()
        return redirect('create_salereceipt', salereceipt_id=salereceipt.id)

    if request.method == 'POST':
        form = Sales_Reciept_ProductForm(request.POST, salereceipt=salereceipt)
        form_salereceipt = Sales_RecieptForm(request.POST, instance=salereceipt)
        if form.is_valid() and form_salereceipt.is_valid():
            salercpt=form_salereceipt.save(commit=False)
            salercpt.created_by=request.user
            salercpt.save()
            salereceipt_product = form.save(commit=False)
            salereceipt_product.salereceipt = salereceipt
            salereceipt_product.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
                rendered_products = render_to_string('salereceipt/salereceipt_product_list.html', {
                    'salereceipt_products': salereceipt_products,
                    'salereceipt_id': salereceipt.id,
                })
                return JsonResponse({
                    'success': True,
                    'rendered_products': rendered_products,
                    'salereceipt_id': salereceipt.id,
                })
            return redirect('edit_salereceipt', salereceipt_id=salereceipt.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors,
                })
    else:
        form = Sales_Reciept_ProductForm(salereceipt=salereceipt)
        form_salereceipt = Sales_RecieptForm(instance=salereceipt)

    salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
    return render(request, 'sale/edit_salereceipt.html', {
        'form': form,
        'salereceipt_products': salereceipt_products,
        'form_salereceipt': form_salereceipt,
        'salereceipt': salereceipt,
        'update':update
    })

@login_required
def delete_salereceipt_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(Sales_Reciept_Product, id=id)
        salereceipt_id = request.POST.get('salereceipt_id')
        product.delete()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def cancel_salereceipt(request,id):
    # salereceipt_id=(request.GET.get('salereceipt_id'))
    salereceipt=get_object_or_404(Sales_Reciept,id=id)
    salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
    # 
    if salereceipt_products:
        for item in salereceipt_products:
            item.delete()
    salereceipt.delete()
    messages.success(request, "Your sale receipt canceled !") 
    return redirect('list_sales')


def delete_salereceipt(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        salereceipt = get_object_or_404(Sales_Reciept, id=id)
        salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
        if salereceipt_products:
            salereceipt_products.delete()  # Bulk delete all related products
        salereceipt.delete()
        return JsonResponse({'success': True, 'message': 'Sale reciept deleted successfully!'})
    
    # For non-AJAX requests, handle as usual
    salereceipt = get_object_or_404(Sales_Reciept, id=id)
    salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
    if salereceipt_products:
        salereceipt_products.delete()  # Bulk delete all related products
    salereceipt.delete()
    messages.success(request, "Sale reciept deleted successfully!")
    return redirect('list_salereceipts')

@login_required
def print_salereceipt(request, salereceipt_id):
    # Fetch the salereceipt instance by ID
    salereceipt = get_object_or_404(Sales_Reciept, id=salereceipt_id)
    # Fetch all products associated with this salereceipt
    salereceipt_products = Sales_Reciept_Product.objects.filter(salereceipt=salereceipt)
    total_amount=salereceipt_products.aggregate(Sum('amount'))
    print(total_amount)

    return render(request, 'sale/print_salereceipt.html', {
        'salereceipt': salereceipt,
        'salereceipt_products': salereceipt_products,
        'total_amount':total_amount
        
    })
