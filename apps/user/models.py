from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from apps.custom_admin.models import Department
from .manager import UserManager

# Create your models here.



class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('User','User'),
        ('Admin','Admin'),
    )
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=10,unique=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    role = models.CharField( max_length=5, choices=ROLE_CHOICES,default='User')
    created_by = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email' or 'phone_number'
    REQUIRED_FIELDS=['name','phone_number']
    objects = UserManager()
    
    def _str_(self):
        return self.name
        
    
    


