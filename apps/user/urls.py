from django.urls import path
from .views import home, login


urlpatterns = [
    path( '' , home , name = 'user_home' ),
    path( 'login/' , login , name = 'user_login' ),
]



