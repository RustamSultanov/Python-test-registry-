from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
import django.urls


urlpatterns = [
 path('', views.base, name='base'),
 path('login', auth_view.LoginView.as_view(template_name='auth_form.html'), name='login'),
 path('logout', auth_view.LogoutView.as_view(next_page="base"), name='logout'),
 path('lichniy-kabinet', views.lichniy_kabinet, name='lichniy-kabinet'),
 path('lichniy-kabinet/<int:comment_id>-comment', views.lk_comment, name='lk_comment'),
 path('delete-<int:comment_id>', views.delete_comment, name='delete_comment'),
 path('add-comment', views.add_comment, name='add_comment'),
 path('lk-accept', views.lk_accept, name='lk_accept'),
 path('lk-accept/accept-<int:comment_id>-comment', views.accept_comment, name='accept_comment'),
]
