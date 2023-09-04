from django.contrib import admin
from django.urls import path
from app.user import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userList/', userListView , name="userListView"),
    path('userLogin/', userLoginView , name="userLoginView"),
    path('userRegister/', userRegisterView , name="userRegisterView"),
]
