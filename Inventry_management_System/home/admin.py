from django.contrib import admin

from .models import Blog,Category,Product,GatePass,GatePassProduct

# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''

    list_display = ['id','title','description']
   

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('productname',)

    search_fields = ('productname',)
