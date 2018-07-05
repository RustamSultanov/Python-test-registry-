from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
import django.urls


urlpatterns = [
 path('', views.base, name='base'),
 path('login', auth_view.LoginView.as_view(template_name='auth_form.html'), name='login'),
 path('logout', auth_view.LogoutView.as_view(next_page="base"), name='logout'),
 path('lichniy-kabinet', views.lichniy_kabinet, name='lichniy-kabinet'),
 path('lichniy-kabinet/<int:ad_id>-comment', views.lk_comment, name='lk_comment'),
 path('delete-<int:ad_id>', views.delete_comment, name='delete_comment'),
]
