from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import User

class AuthBackend(BaseBackend):
    def authenticate(*credentials):
        try:
            try:
                user = User.objects.get(email=credentials[0])
            except:
                user = User.objects.get(phone_number=credentials[0])
        except:
            return None
        password_valid = check_password(credentials[1],user.password)
        if user and password_valid:
            return user
        return None 
