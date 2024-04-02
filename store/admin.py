from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Product)


class StoreAdminSite(admin.AdminSite):
    site_header = "Store Admin"
    site_title = "Store Portal"
    index_title = "Welcome to My Ecommerece"


store_admin_site = StoreAdminSite(name="store_admin")


store_admin_site.register(Product)
