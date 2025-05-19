from django.contrib import admin
from .models import CustomUser,VendorProfile

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','is_active','is_verified','name','email','password','phone','address','image']

@admin.register(VendorProfile)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','is_active','is_verified','name','email','password','shop_name','phone','gst_number','shop_logo','website']