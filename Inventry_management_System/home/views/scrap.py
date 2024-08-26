
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from ..forms import  GatePassProductForm,GatePassForm
from ..models import GatePass, GatePassProduct,Product
from django.contrib import messages

product_list=[]

@login_required
def gatepass(request):

    if 'gatepass_products' in request.session:
        del request.session['gatepass_products']

    form = GatePassProductForm()
    form_gatepass=GatePassForm()
    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass':form_gatepass,   
    })

# @login_required
# def create_gatepass(request, gatepass_id=None):
#     if gatepass_id:
#         gatepass = get_object_or_404(GatePass, id=gatepass_id)
#     else:
#         gatepass = GatePass.objects.create()
#         print('i m here 222')
#         if request.method == 'POST':
#             form = GatePassProductForm(request.POST)
#             form_gatepass = GatePassForm(request.POST, instance=gatepass)
#             if form.is_valid() and form_gatepass.is_valid():
#                 # Update the GatePass object with the form_gatepass data
#                 form_gatepass.save()  # This will update the existing instance
                
#                 # Save the GatePassProduct object and associate it with the updated GatePass
#                 gatepass_product = form.save(commit=False)
#                 gatepass_product.gatepass = gatepass
#                 gatepass_product.save()
#                 return redirect('create_gatepass', gatepass_id=gatepass.id)

#     if request.method == 'POST':
#         print('i m here')
#         form = GatePassProductForm(request.POST)
#         form_gatepass = GatePassForm(request.POST, instance=gatepass)
#         if form.is_valid() and form_gatepass.is_valid():
#             # Update the GatePass object with the form_gatepass data
#             form_gatepass.save()  # This will update the existing instance
            
#             # Save the GatePassProduct object and associate it with the updated GatePass
#             gatepass_product = form.save(commit=False)
#             gatepass_product.gatepass = gatepass
#             gatepass_product.save()
#             return redirect('create_gatepass', gatepass_id=gatepass.id)
#     else:
#         form = GatePassProductForm()
#         form_gatepass=GatePassForm(instance=gatepass)
#     gatepass_products = GatePassProduct.objects.filter(gatepass=gatepass)
#     return render(request, 'gatepass/create_gatepass.html', {
#         'form': form,
#         'gatepass_products': gatepass_products,
#         'form_gatepass':form_gatepass,
#         'gatepass': gatepass,
#     })
'''
@login_required
def create_gatepass(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = None
    if request.method == 'POST':
        form_gatepass = GatePassForm(request.POST, instance=gatepass)
        form = GatePassProductForm(request.POST)

        if 'add_product' in request.POST:
            if form.is_valid():
                gatepass_products = request.session.get('gatepass_products', [])
                product_id = form.cleaned_data['product'].id
                quantity = form.cleaned_data['quantity']
                remarks = form.cleaned_data['remarks']
                pro=get_object_or_404(Product, id=product_id)
                unit=pro.unit.name
                weight=int(pro.product_weight)*int(quantity)
                
                print(gatepass_products,type(gatepass_products))

                for i in gatepass_products:
                    print(i['product_id'])
                    if i['product_id']==form.cleaned_data['product'].id:
                        print("product already added")
                        
                    else:
                        print("product added successfuly")
                        break
                        
                gatepass_products.append({
                            'product_id': product_id,
                            'product_name': form.cleaned_data['product'].productname,
                            'quantity': quantity,
                            'unit':unit,
                            "weight":weight,
                            'remarks': remarks,
                            
                        })

                request.session['gatepass_products'] = gatepass_products
                form = GatePassProductForm()

        elif 'finalize_gatepass' in request.POST:
            if form_gatepass.is_valid():
                if not gatepass:
                    gatepass = form_gatepass.save()
                else:
                    form_gatepass.save()

                gatepass_products = request.session.pop('gatepass_products', [])
                for gp in gatepass_products:
                    product = get_object_or_404(Product, id=gp['product_id'])
                  
                    GatePassProduct.objects.create(
                        gatepass=gatepass,
                        product=product,
                        quantity=gp['quantity'],
                        remarks=gp['remarks']
                    )
                return redirect('list_gatepasses')

    else:
        form = GatePassProductForm()
        form_gatepass = GatePassForm(instance=gatepass)

    gatepass_products = request.session.get('gatepass_products', [])

    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass': form_gatepass,
        'gatepass_products': gatepass_products,
        'gatepass': gatepass,
    })
    
'''

def create_gatepass(request, gatepass_id=None):
    if gatepass_id:
        gatepass = get_object_or_404(GatePass, id=gatepass_id)
    else:
        gatepass = None

    # Initialize form_gatepass with GET or POST data
    form_gatepass = GatePassForm(request.POST or None, instance=gatepass)
    
    if request.method == 'POST':
        form = GatePassProductForm(request.POST)

        if 'add_product' in request.POST:
            if form.is_valid():
                gatepass_products = request.session.get('gatepass_products', [])
                product_id = form.cleaned_data['product'].id

                # Check if the product is already in the gatepass
                existing_product = next((gp for gp in gatepass_products if gp['product_id'] == product_id), None)

                if existing_product:
                    # If product exists, update its quantity and remarks
                    # existing_product['quantity'] += form.cleaned_data['quantity']
                    # existing_product['remarks'] = form.cleaned_data['remarks']
                    print('product already in gatepass')
                    messages.success(request, 'Product already in gatepass')
                else:

                    pro=get_object_or_404(Product, id=product_id)
                    unit=pro.unit.name
                    weight=int(pro.product_weight)*int(form.cleaned_data['quantity'])
                    # If product doesn't exist, add it to the session
                    gatepass_products.append({
                        'product_id': product_id,
                        'product_name': form.cleaned_data['product'].productname,
                        'quantity': form.cleaned_data['quantity'],
                        'unit':unit,
                        "weight":weight,
                        'remarks': form.cleaned_data['remarks'],
                    })
                    print('product in gatepass')

                request.session['gatepass_products'] = gatepass_products

        elif 'finalize_gatepass' in request.POST:
            if form_gatepass.is_valid():
                if not gatepass:
                    gatepass = form_gatepass.save()
                else:
                    form_gatepass.save()

                gatepass_products = request.session.pop('gatepass_products', [])
                for gp in gatepass_products:
                    product = get_object_or_404(Product, id=gp['product_id'])
                    
                    GatePassProduct.objects.create(
                        gatepass=gatepass,
                        product=product,
                       
                        quantity=gp['quantity'],
                        remarks=gp['remarks']
                    )
                return redirect('list_gatepasses')

    else:
        form = GatePassProductForm()

    gatepass_products = request.session.get('gatepass_products', [])

    return render(request, 'gatepass/create_gatepass.html', {
        'form': form,
        'form_gatepass': form_gatepass,
        'gatepass_products': gatepass_products,
        'gatepass': gatepass,
    })

from django.http import JsonResponse
@login_required
def clear_session(request):
    if 'gatepass_products' in request.session:
        del request.session['gatepass_products']
    return JsonResponse({'status': 'success'})


def edit_gatepass_product(request, product_id):
    gatepass_products = request.session.get('gatepass_products', [])
    product_to_edit = None

    for product in gatepass_products:
        if product['product_id'] == product_id:
            product_to_edit = product
            break

    if not product_to_edit:
        return redirect('create_gatepass')

    if request.method == 'POST':
        form = GatePassProductForm(request.POST)
        if form.is_valid():
            product_to_edit['product_id'] = form.cleaned_data['product'].id
            product_to_edit['product_name'] = form.cleaned_data['product'].productname
            product_to_edit['quantity'] = form.cleaned_data['quantity']
            product_to_edit['remarks'] = form.cleaned_data['remarks']

            request.session['gatepass_products'] = gatepass_products
            return redirect('create_gatepass')

    else:
        form = GatePassProductForm(initial={
            'product': product_to_edit['product_id'],
            
            'quantity': product_to_edit['quantity'],
            'remarks': product_to_edit['remarks'],
        })

    form_gatepass = GatePassForm(instance=request.session.get('gatepass_instance', None))

    return render(request, 'gatepass/edit_gatepass_product.html', {
        'form': form,
        'form_gatepass': form_gatepass
    })

def delete_gatepass_product(request, product_id):
    gatepass_products = request.session.get('gatepass_products', [])
    gatepass_products = [product for product in gatepass_products if product['product_id'] != product_id]
    request.session['gatepass_products'] = gatepass_products
    form_gatepass = GatePassForm(instance=request.session.get('gatepass_instance', None))
    return redirect('create_gatepass')


@login_required
def list_gatepasses(request):
    gatepasses = GatePass.objects.all()
    return render(request, 'gatepass/list_gatepasses.html', {'gatepasses': gatepasses})

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