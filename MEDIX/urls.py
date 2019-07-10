"""MEDIX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import register_new_user,register_new_hospital,register_new_vendor,user_and_hospital_login,vendor_login,all_logout
from main_app.views import MedicineSearchView,VendorsView,vendor_add_medicine,vendor_delete_medicine,vendor_update_medicine
urlpatterns = [
    path('admin/', admin.site.urls),
    path('normal_user_register/', register_new_user),
    path('hospital_register/',register_new_hospital),
    path('vendor_register/',register_new_vendor),
    path('user_hospital_login/',user_and_hospital_login,name='u_h_login'),
    path('vendor_login/',vendor_login,name='v_login'),
    path('search_page/',MedicineSearchView,name="m_search"),
    path('logout/',all_logout,name='log_out'),
    path('vendor_page/',VendorsView),
    path('add_medicine/',vendor_add_medicine),
    path('remove_medicine/<id>',vendor_delete_medicine),
    path('update_medicine/<id>',vendor_update_medicine),
]
