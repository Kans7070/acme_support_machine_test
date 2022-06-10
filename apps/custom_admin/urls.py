from django.urls import path
from .views import create_department, create_user, delete_department, department, edit_department, home,login,logout


urlpatterns = [
    path( '' , home , name = 'admin_home' ),
    path( 'department/' , department , name = 'department_page' ),
    path( 'login/' , login , name = 'admin_login' ),
    path( 'logout/' , logout , name = 'logout' ),
    path( 'create_user/' , create_user , name = 'admin_create_user' ),
    path( 'create_department/' , create_department , name = 'admin_create_department' ),
    path( 'edit_department/<int:pk>' , edit_department , name = 'admin_edit_department' ),
    path( 'delete_department/<int:pk>' , delete_department , name = 'admin_delete_department' ),
]

