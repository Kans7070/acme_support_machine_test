from django.db import models

class DepartmentManager(models.Manager):
    def create_department(self, name, description,created_by):
        if not name:
            raise ValueError("user must have an name")

        departmant = self.model(
            name=name,
            description=description,
            created_by=created_by
        )

        departmant.save()
        return departmant
