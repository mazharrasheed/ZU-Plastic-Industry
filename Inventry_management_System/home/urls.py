from django.contrib import admin
from django.urls import  path
from home.views import category,product
from home.views import views,accounts
from home.views import gatepass,sales,suppliers

from django.conf.urls.static import static

from Inventry_management_System import settings

urlpatterns = [
   
    path('', views.index,name="index"),
    path('dashboard/', views.dashboard,name="dashboard"),
    path('postblog/', views.post_blog,name="postblog"),
    path('signup/', views.sign_up,name="signup"),
    path('signin/', views.sign_in,name="signin"),
    path('login/', views.sign_in,name="signin"),
    # path('accounts/login/', views.sign_in,name="signin"),@login requried hit this url
    path('logout/', views.log_out,name="logout"),
    path('detail/<int:id>', views.detail,name="detail"),
    path('delete/<int:id>', views.delete_data , name="deletedata"),
    path('edit/<int:id>', views.edit_data , name="editdata"),
    path('editprofile/<int:id>', views.editprofile , name="editprofile"),

    path('category/', category.add_category , name="category"),
    path('category/<int:id>', category.edit_category , name="editcategory"),
    path('deletecategory/<int:id>', category.delete_category , name="deletecategory"),

    path('product/', product.products , name="product"),
    path('add_product/', product.add_product , name="addproduct"),
    path('product/<int:id>', product.edit_product , name="editproduct"),
    path('deleteproduct/<int:id>', product.delete_product , name="deleteproduct"),

    path('suppliers/', suppliers.supplier , name="suppliers"),
    path('add_supplier/', suppliers.add_supplier , name="addsupplier"),
    path('supplier/<int:id>', suppliers.edit_supplier , name="editsupplier"),
    path('deletesupplier/<int:id>', suppliers.delete_supplier , name="deletesupplier"),
    
    path('gatepass/', gatepass.gatepass , name="gatepass"),
    path('create-gatepass/', gatepass.create_gatepass, name='create_gatepass'),
    path('create-gatepass/<int:gatepass_id>/', gatepass.create_gatepass, name='create_gatepass'),
    path('edit-gatepass/<int:gatepass_id>/', gatepass.edit_gatepass, name='edit_gatepass'),
    path('cancel_gatepass/<int:id>/', gatepass.cancel_gatepass, name='cancel_gatepass'),
    path('delete_gatepass/<int:id>/', gatepass.delete_gatepass, name='delete_gatepass'),
    path('delete_gatepass_item/<int:id>/', gatepass.delete_gatepass_item, name='delete_gatepass_item'),
    path('list-gatepasses/', gatepass.list_gatepasses, name='list_gatepasses'),
    path('print-gatepass/<int:gatepass_id>/', gatepass.print_gatepass, name='print_gatepass'),


    path('salereceipt/', sales.salereceipt , name="salereceipt"),
    path('create-salereceipt/', sales.create_salereceipt, name='create_salereceipt'),
    path('create-salereceipt/<int:salereceipt_id>/', sales.create_salereceipt, name='create_salereceipt'),
    path('edit-salereceipt/<int:salereceipt_id>/', sales.edit_salereceipt, name='edit_salereceipt'),
    path('cancel_salereceipt/<int:id>/', sales.cancel_salereceipt, name='cancel_salereceipt'),
    path('delete_salereceipt/<int:id>/', sales.delete_salereceipt, name='delete_salereceipt'),
    path('delete_salereceipt_item/<int:id>/', sales.delete_salereceipt_item, name='delete_salereceipt_item'),
    path('list-sales/', sales.list_sales, name='list_sales'),
    path('print-salereceipt/<int:salereceipt_id>/', sales.print_salereceipt, name='print_salereceipt'),



    path('accounts/', accounts.accounts , name="accounts"),
    path('add_accounts/', accounts.add_account , name="add_accounts"),
    path('editaccount/<int:id>', accounts.edit_account , name="editaccount"),
    path('deleteaccount/<int:id>', accounts.delete_account , name="deleteaccount"),
    path('accountreport/<int:id>', accounts.account_report , name="accountreport"),

    path('transaction/', accounts.add_transaction , name="transaction"),
    path('edittransaction/<int:id>', accounts.edit_transaction , name="edittransaction"),
    path('deletetransaction/<int:id>', accounts.delete_transaction , name="deletetransaction"),
    path('balance_sheet/', accounts.balance_sheet , name="balancesheet"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
