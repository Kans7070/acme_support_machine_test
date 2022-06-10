from django.db import models

from .manager import DepartmentManager



# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=50)
    created_by = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True,null=True,blank=True)
    last_updated = models.DateField(null=True,blank=True)
    object = DepartmentManager()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'department'
