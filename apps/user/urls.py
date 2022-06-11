from django.urls import path
from .views import home, login,user_create_ticket


urlpatterns = [
    path( '' , home , name = 'user_home' ),
    path('create_ticket/',user_create_ticket,name = 'user_create_ticket'),
    path( 'login/' , login , name = 'user_login' ),
]



