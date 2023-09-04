from django.contrib import admin
from django.urls import path
from app1.user import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userList/', userListView , name="userListView"),
    path('userLogin/', userLoginView , name="userLoginView"),
    path('userRegister/', userRegisterView , name="userRegisterView"),
]
