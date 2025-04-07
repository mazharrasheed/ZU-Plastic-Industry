# Create your views here.

from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  Sales_Receipt_ProductForm,Sales_ReceiptForm,Sales_Cash_Receipt_ProductForm,Sales_Cash_ReceiptForm
from ..models import Sales_Receipt, Sales_Receipt_Product,Product,Product_Price,Transaction,Account,Customer
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg,Min,Max,Count,Sum
from collections import defaultdict
from django.db import transaction


@login_required
@permission_required('home.view_sales_receipt', login_url='/login/')
def list_sales(request):
    salereceipt_items_pro = {}
    total_amount = {}
    salereceipts=[]
    customer=(request.GET.get('customer'))
    cash=(request.GET.get('cash'))
    if customer=="True":
        customer=True
        salereceipts = Sales_Receipt.objects.filter(is_cash=False)
    elif cash=="True":
        cash=True
        salereceipts = Sales_Receipt.objects.filter(is_cash=True)
    else:
        salereceipts = Sales_Receipt.objects.all()
        
    for x in salereceipts:
        # Count the number of products for each sale receipt
        salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
        # Get products for the sale receipt and aggregate the amount
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
        total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))

    total_sale = sum(item['amount__sum'] or 0 for item in total_amount.values())

    return render(request, 'sale/list_sales.html', {
        'salereceipts': salereceipts,
        'salereceipt_items_pro': salereceipt_items_pro,
        'total_amount': total_amount,
        'total_sale':total_sale,
        'customer':customer,
        'cash':cash,
    })

@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def salereceipt(request):
    form = Sales_Receipt_ProductForm()
    form_salereceipt=Sales_ReceiptForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_salereceipt':form_salereceipt,   
    })


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def create_salereceipt(request, salereceipt_id=None):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        if 'finalize' in request.POST:
            form_salereceipt = Sales_ReceiptForm(request.POST)
            products = request.POST.getlist('products[]')

            if form_salereceipt.is_valid() and products:
                customer = form_salereceipt.cleaned_data.get('customer_name')
                product_objects = []

                # Validate all product prices before saving anything
                for product_data in products:
                    try:
                        product_id, quantity = product_data.split(':')
                        product = Product.objects.get(id=product_id)
                        quantity = int(quantity)
                        unit_price_cust = Product_Price.objects.get(
                            is_deleted=False,
                            customer=customer,
                            product=product
                        )
                        unit_price = float(unit_price_cust.price)
                        amount = unit_price * quantity

                        product_objects.append({
                            'product': product,
                            'quantity': quantity,
                            'unit_price': unit_price,
                            'amount': amount,
                        })

                    except Product.DoesNotExist:
                        return JsonResponse({'success': False, 'errors': f'Product with ID {product_id} not found.'})
                    except Product_Price.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'price': False,
                            'errors': f'No price found for product "{product.productname}" for this customer.'
                        })
                    except Exception as e:
                        return JsonResponse({'success': False, 'errors': str(e)})

                # Save the receipt and products atomically
                try:
                    with transaction.atomic():
                        salercpt = form_salereceipt.save(commit=False)
                        salercpt.created_by = request.user
                        salercpt.save()

                        for item in product_objects:
                            Sales_Receipt_Product.objects.create(
                                salereceipt=salercpt,
                                product=item['product'],
                                quantity=item['quantity'],
                                unit_price=item['unit_price'],
                                amount=item['amount']
                            )

                    return JsonResponse({'success': True, 'redirect_url': '/list-sales?customer=True'})
                except Exception as e:
                    return JsonResponse({'success': False, 'errors': str(e)})

            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = Sales_Receipt_ProductForm()
        form_salereceipt = Sales_ReceiptForm()

    return render(request, 'sale/create_salereceipt.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
    })


@login_required
@permission_required('home.change_sales_receipt', login_url='/login/')


def edit_salereceipt(request, salereceipt_id=None):
    salercpt = get_object_or_404(Sales_Receipt, id=salereceipt_id)
    products = Sales_Receipt_Product.objects.filter(salereceipt=salercpt.id)

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = Sales_ReceiptForm(request.POST, instance=salercpt)
        if form.is_valid():
            customer = form.cleaned_data.get('customer_name')
            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')

            product_quantities = defaultdict(int)
            validated_products = []

            # Validate all incoming product data and check for required prices
            for product_info in product_data:
                try:
                    product_id, quantity = product_info.split(':')
                    quantity = int(quantity)
                    product = Product.objects.get(id=product_id)
                    unit_price_cust = Product_Price.objects.get(is_deleted=False, customer=customer, product=product)
                    unit_price = float(unit_price_cust.price)
                    amount = unit_price * quantity

                    product_quantities[product_id] += quantity

                    validated_products.append({
                        'product': product,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'amount': amount,
                    })
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with ID {product_id} does not exist.'})
                except Product_Price.DoesNotExist:
                    return JsonResponse({'success': False, 'price': False, 'message': f'No price found for product "{product.productname}" for this customer.'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})

            try:
                with transaction.atomic():
                    form.save()

                    # Delete removed products
                    Sales_Receipt_Product.objects.filter(salereceipt=salercpt, product__id__in=deleted_products).delete()

                    # Update or create all validated products
                    for item in validated_products:
                        Sales_Receipt_Product.objects.update_or_create(
                            salereceipt=salercpt,
                            product=item['product'],
                            defaults={
                                'quantity': product_quantities[str(item['product'].id)],
                                'unit_price': item['unit_price'],
                                'amount': item['unit_price'] * product_quantities[str(item['product'].id)],
                            }
                        )

                return JsonResponse({'success': True, 'redirect_url': '/list-sales?customer=True'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    context = {
        'salereceipt': salercpt,
        'products': products,
        'form_salereceipt': Sales_ReceiptForm(instance=salercpt),
        'form': Sales_Receipt_ProductForm(),
    }
    return render(request, 'sale/edit_salereceipt.html', context)

@login_required
@permission_required('home.delete_sales_receipt', login_url='/login/')
def delete_salereceipt_item(request,id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        product = get_object_or_404(Sales_Receipt_Product, id=id)
        salereceipt_id = request.POST.get('salereceipt_id')
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def create_cash_salereceipt(request, salereceipt_id=None):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'finalize' in request.POST:  # Finalize the purchase note
            form_salereceipt = Sales_Cash_ReceiptForm(request.POST)
            products = request.POST.getlist('products[]')
            if form_salereceipt.is_valid() and products:
                salercpt = form_salereceipt.save(commit=False)
                salercpt.created_by = request.user
                salercpt.is_cash = True
                salercpt.save()
                for product_data in products:
                    product_id, quantity , unit_price, amount= product_data.split(':')
                    Sales_Receipt_Product.objects.create(
                        salereceipt=salercpt,
                        product_id=product_id,
                        quantity=quantity,
                        unit_price=unit_price,
                        amount=amount
                    )
                    
                return JsonResponse({'success': True, 'redirect_url': '/list-sales?cash=True'})
            else:
                return JsonResponse({'success': False, 'errors': 'Invalid form data or no products selected.'})
    else:
        form = Sales_Cash_Receipt_ProductForm()
        form_salereceipt = Sales_Cash_ReceiptForm()
    return render(request, 'sale/create_cash_salereceipt.html', {
        'form': form,
        'form_salereceipt': form_salereceipt,
    })


@login_required
@permission_required('home.change_sales_receipt', login_url='/login/')
def edit_cash_salereceipt(request, salereceipt_id=None):
    salercpt = get_object_or_404(Sales_Receipt, id=salereceipt_id)
    products = Sales_Receipt_Product.objects.filter(salereceipt=salercpt.id)
    if request.method == 'POST':
        form = Sales_Cash_ReceiptForm(request.POST, instance=salercpt)
        if form.is_valid():
            grn = form.save()
            product_data = request.POST.getlist('products[]')
            deleted_products = request.POST.getlist('deleted_products[]')
            # Delete removed products
            Sales_Receipt_Product.objects.filter(salereceipt=salercpt, product__id__in=deleted_products).delete()
            product_quantities = defaultdict(int)
            for product_info in product_data:
                try:
                    product_id, quantity,unit_price,amount = product_info.split(':')
                    product_quantities[product_id] += int(quantity)
                except ValueError:
                    return JsonResponse({'success': False, 'message': 'Invalid product data.'})

            for product_id, total_quantity in product_quantities.items():
        
                try:
                    product_id, quantity,unit_price,amount = product_info.split(':')
                    product_instance = Product.objects.get(id=product_id)
                    print("product id :",product_id, "qty:",total_quantity,unit_price,amount)
                    product, created = Sales_Receipt_Product.objects.update_or_create(
                        salereceipt=salercpt, 
                        product=product_instance, 
                        defaults={
                            'quantity': total_quantity,
                            'unit_price': float(unit_price),
                            'amount': float(amount),
                        }
                    )
                    
                except Product.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Product with ID {product_id} does not exist.'})

            return JsonResponse({'success': True, 'redirect_url': '/list-sales?cash=True'})

        return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    context = {
        'salereceipt': salercpt,
        'products': products,
        'form_salereceipt': Sales_Cash_ReceiptForm(instance=salercpt),
        'form': Sales_Cash_Receipt_ProductForm(),
    }
    return render(request, 'sale/edit_cash_salereceipt.html', context)


@login_required
@permission_required('home.add_sales_receipt', login_url='/login/')
def cancel_salereceipt(request,id):
    # salereceipt_id=(request.GET.get('salereceipt_id'))
    salereceipt=get_object_or_404(Sales_Receipt,id=id)
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    # 
    if salereceipt_products:
        for item in salereceipt_products:
            item.delete()
    salereceipt.delete()
    messages.success(request, "Your sale receipt canceled !") 
    return redirect('list_sales')

@login_required
@permission_required('home.delete_sales_receipt', login_url='/login/')
def delete_salereceipt(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        salereceipt = get_object_or_404(Sales_Receipt, id=id)
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
        if salereceipt_products:
            salereceipt_products.delete()  # Bulk delete all related products
        salereceipt.delete()
        return JsonResponse({'success': True, 'message': 'Sale receipt deleted successfully!'})
    
    # For non-AJAX requests, handle as usual
    salereceipt = get_object_or_404(Sales_Receipt, id=id)
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    if salereceipt_products:
        salereceipt_products.delete()  # Bulk delete all related products
    salereceipt.delete()
    messages.success(request, "Sale receipt deleted successfully!")
    return redirect('list_salereceipts')

@login_required
@permission_required('home.view_sales_receipt', login_url='/login/')
def print_salereceipt(request, salereceipt_id):
    # Fetch the salereceipt instance by ID
    salereceipt = get_object_or_404(Sales_Receipt, id=salereceipt_id)
    # Fetch all products associated with this salereceipt
    salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=salereceipt)
    total_amount=salereceipt_products.aggregate(Sum('amount'))
    return render(request, 'sale/print_salereceipt.html', {
        'salereceipt': salereceipt,
        'salereceipt_products': salereceipt_products,
        'total_amount':total_amount
        
    })

def make_transaction(request,id):

    salereceipt_items_pro = {}
    total_amount = {}
    salereceipt = get_object_or_404(Sales_Receipt, id=id)
    salereceipts = Sales_Receipt.objects.all()

    for x in salereceipts:
        # Count the number of products for each sale receipt
        salereceipt_items_pro[x.id] = Sales_Receipt_Product.objects.filter(salereceipt=x).count()
        # Get products for the sale receipt and aggregate the amount
        salereceipt_products = Sales_Receipt_Product.objects.filter(salereceipt=x)
        total_amount[x.id] = salereceipt_products.aggregate(Sum('amount'))
        
    coname=salereceipt.customer_name
    customer=Customer.objects.get(coname=coname, is_deleted=False)
    debit_account=Account.objects.get(customer=customer.id,is_deleted=False)
    credit_account=Account.objects.get(account_type="Revenue",name="Sales",is_deleted=False)
    amt=total_amount[id]
    amount=amt['amount__sum']
    transaction=Transaction(description=f' sales receipt id = {salereceipt.id}',debit_account=debit_account,credit_account=credit_account,amount=amount)
    transaction.save()
    salereceipt.make_transaction=True
    salereceipt.save()
    salereceipts = Sales_Receipt.objects.all()
    total_sale = sum(item['amount__sum'] or 0 for item in total_amount.values())
    messages.success(request, "Transaction added successfully!")

    return render(request, 'sale/list_sales.html', {
        'salereceipts': salereceipts,
        'salereceipt_items_pro': salereceipt_items_pro,
        'total_amount': total_amount,
        'total_sale':total_sale

    })
