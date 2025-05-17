from django.db import models

# Create your models here.
USER_ROLES=(
    
    ('VENDOR','Vendor'),
    ('CUSTOMER','Customer')
)

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
    role=models.CharField(max_length=30,choices=USER_ROLES,default='CUSTOMER')
      
    
    def __str__(self):
        return f'{self.name}'