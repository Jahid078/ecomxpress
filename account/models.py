from django.db import models


class Common(models.Model):
    is_active=models.BooleanField(default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)
    

    class Meta:
        abstract=True


class CustomUser(Common):
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    name=models.CharField(max_length=30,null=True,blank=True)
    phone=models.CharField(max_length=10,null=True,blank=True)
    address=models.CharField(max_length=30,null=True,blank=True)
    image=models.ImageField(upload_to='image/',null=True,blank=True)
    # role=models.CharField(max_length=30,choices=USER_ROLES,default='CUSTOMER')
      
    
    def __str__(self):
        return f'{self.name}'
    
    
class VendorProfile(Common):
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=30,null=True,blank=True)
    password=models.CharField(max_length=30)
    shop_name=models.CharField(max_length=100)
    gst_number=models.IntegerField(null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    shop_address=models.CharField(max_length=30)
    shop_logo=models.ImageField(upload_to='vendors/logo/',null=True,blank=True)
    website=models.URLField(null=True,blank=True)
    
    
    def __str__(self):
        return f'{self.name}'
    