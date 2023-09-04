from django.contrib import admin
from django.urls import path
from blockudokuBack.app1.user import userListView, userLoginView, userRegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('userList/', userListView , name="userListView"),
    path('userLogin/', userLoginView , name="userLoginView"),
    path('userRegister/', userRegisterView , name="userRegisterView"),
]
