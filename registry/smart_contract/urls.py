from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
import django.urls


urlpatterns = [
 path('', views.base, name='base'),
 path('accounts/login/', auth_view.LoginView.as_view(template_name='auth_form.html'), name='login'),
 path('logout', auth_view.LogoutView.as_view(next_page="base"), name='logout'),
 path('regist-employee', views.registration_view, name='regist_employee'),
 path('employee-list', views.employee_list, name='employee_list'),
 path('employee-list/<int:user_id>', views.employee_info, name='employee_info'),
 path('lk-comment-list', views.lichniy_kabinet, name='lichniy-kabinet'),
 path('lk-competence', views.competence_list, name='competence_list'),
 path('lk-comment-list/<int:comment_id>-comment', views.lk_comment, name='lk_comment'),
 path('delete-<int:comment_id>', views.delete_comment, name='delete_comment'),
 path('add-comment', views.add_comment, name='add_comment'),
 path('lk-accept', views.lk_accept, name='lk_accept'),
 path('lk-accept/accept-<int:comment_id>-comment', views.accept_comment, name='accept_comment'),
 path('lk-accepted-list/info-<int:comment_id>-comment', views.comment_info, name='comment_info'),
 path('lk-failure/failure-<int:comment_id>-comment', views.lk_failure, name='lk_failure'),
 path('genres/', views.show_genres, name='show_genres'),
]
