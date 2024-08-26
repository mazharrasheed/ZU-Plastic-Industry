from django.contrib import admin
from django.urls import  path
from home.views import category,product
from home.views import views,accounts
from home.views import gatepass

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
    
    path('gatepass/', gatepass.gatepass , name="gatepass"),
    path('create-gatepass/', gatepass.create_gatepass, name='create_gatepass'),
    path('create-gatepass/<int:gatepass_id>/', gatepass.create_gatepass, name='create_gatepass'),
    path('edit-gatepass/<int:gatepass_id>/', gatepass.edit_gatepass, name='edit_gatepass'),
    path('cancel_gatepass/<int:id>/', gatepass.cancel_gatepass, name='cancel_gatepass'),
    path('delete_gatepass/<int:id>/', gatepass.delete_gatepass, name='delete_gatepass'),
    path('delete_gatepass_item/<int:id>/', gatepass.delete_gatepass_item, name='delete_gatepass_item'),
    path('update_delete_gatepass_item/<int:id>/', gatepass.update_delete_gatepass_item, name='update_delete_gatepass_item'),
    path('list-gatepasses/', gatepass.list_gatepasses, name='list_gatepasses'),
    path('print-gatepass/<int:gatepass_id>/', gatepass.print_gatepass, name='print_gatepass'),

    path('accounts/', accounts.add_account , name="accounts"),
    path('editaccount/<int:id>', accounts.edit_account , name="editaccount"),
    path('deleteaccount/<int:id>', accounts.delete_account , name="deleteaccount"),
    path('accountreport/<int:id>', accounts.account_report , name="accountreport"),

    path('transaction/', accounts.add_transaction , name="transaction"),
    path('edittransaction/<int:id>', accounts.edit_transaction , name="edittransaction"),
    path('deletetransaction/<int:id>', accounts.delete_transaction , name="deletetransaction"),
    path('balance/', accounts.balance_sheet , name="balance"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
