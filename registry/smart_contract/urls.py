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
 path('comment-list', views.comment_list, name='comment_list'),
 path('competence', views.competence_list, name='competence_list'),
 path('comment-list/<int:comment_id>-comment', views.edit_comment, name='edit_comment'),
 path('delete-<int:comment_id>', views.delete_comment, name='delete_comment'),
 path('add-comment', views.add_comment, name='add_comment'),
 path('accept', views.accept_list, name='accept_list'),
 path('accept/accept-<int:comment_id>-comment', views.accept_comment, name='accept_comment'),
 path('accepted-list/info-<int:comment_id>-comment', views.comment_info, name='comment_info'),
 path('failure/failure-<int:comment_id>-comment', views.failure_comment, name='failure_comment'),
 path('genres/', views.show_genres, name='show_genres'),
]
