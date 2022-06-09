from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self,name,email,phone_number,password,department,created_by ):
        if not name:
            raise ValueError('user must have an name')

        if not email:
            raise ValueError('user must have an email')

        if not phone_number:
            raise ValueError('user must have an phone')
        
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            department=department,
            created_by=created_by,
        )
        user.role = 'User'
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,name,email,phone_number,password):
        if not name:
            raise ValueError('user must have an name')

        if not email:
            raise ValueError('user must have an email')

        if not phone_number:
            raise ValueError('user must have an phone')
        
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.role = 'Admin'
        user.set_password(password)
        user.save()
        return user