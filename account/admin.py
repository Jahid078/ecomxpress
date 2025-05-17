from django.contrib import admin
from .models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','is_active','is_verified','name','email','phone','address','role']