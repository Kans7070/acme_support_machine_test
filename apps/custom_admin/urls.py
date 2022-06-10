from django.urls import path
from .views import admin_create_ticket,admin_ticket, create_department, create_user, delete_department, department, edit_department, home,login,logout


urlpatterns = [
    path( '' , home , name = 'admin_home' ),
    path( 'department/' , department , name = 'department_page' ),
    path( 'ticket/' , admin_ticket , name = 'admin_ticket_page' ),
    path( 'login/' , login , name = 'admin_login' ),
    path( 'logout/' , logout , name = 'logout' ),
    path( 'create_user/' , create_user , name = 'create_user' ),
    path( 'create_department/' , create_department , name = 'create_department' ),
    path( 'create_ticket/' , admin_create_ticket , name = 'admin_create_ticket' ),
    path( 'edit_department/<int:pk>' , edit_department , name = 'edit_department' ),
    path( 'delete_department/<int:pk>' , delete_department , name = 'delete_department' ),

]

