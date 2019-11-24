from django.urls import path, reverse, reverse_lazy
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView

from . import views
from . import forms


urlpatterns = [
 path('registration-admin', views.RegistrationUser.as_view(form_class=forms.RegistrationEmployeeForm), name='registration_admin'),
 path('', TemplateView.as_view(template_name="index.html"), name='base'),
 path('registration-company', views.RegistrationCompany.as_view(), name='registration_company'),
 path('additional-registration-company', views.AdditionalRegistrationCompany.as_view(), name='additional_registration_company'),
 path('registration-finaly', views.RegistrationAcceptUser.as_view(), name='registration_finaly'),
 path('successe_registration', TemplateView.as_view(template_name="django_registration/registration_success.html"), name='successe_registration'),
 path('edit-company', views.EditCompany.as_view(), name='edit_company'),
 path('accounts/login/', auth_view.LoginView.as_view(template_name='django_registration/auth_form.html'), name='login'),
 path('logout', auth_view.LogoutView.as_view(next_page="base"), name='logout_custom'),
 path('registration-employee/<int:company_id>', views.RegistrationEmployee.as_view(form_class=forms.RegistrationEmployeeForm), name='registration_user'),
 path('login-after-registation', views.LoginAfterRegistration.as_view(template_name='django_registration/login_after_registration.html'), name='login_after_registation'),
 path('employee-list', views.employee_list, name='employee_list'),
 path('employee-list/<int:user_id>', views.employee_info, name='employee_info'),
 path('comment-list', views.comment_list, name='comment_list'),
 path('competence', views.competence_list, name='competence_list'),
 path('comment-list/<int:comment_id>-comment', views.edit_comment, name='edit_comment'),
 path('delete-<int:comment_id>', views.delete_comment, name='delete_comment'),
 path('check-company', views.CheckCompanyBeforeComment.as_view(), name='check_company'),
 path('invitation-company', views.InvitationCompany.as_view(), name='invitation_company'),
 path('invitation-employee', views.InvitationEmployee.as_view(), name='invitation_employee'),
 path('success-send-invitation', TemplateView.as_view(template_name="success_send_invitation.html"), name='success_send_invitation'),
 path('add-comment', views.add_comment, name='add_comment'),
 path('accept', views.accept_list, name='accept_list'),
 path('accept/accept-<int:comment_id>-comment', views.accept_comment, name='accept_comment'),
 path('accepted-list/info-<int:comment_id>-comment', views.comment_info, name='comment_info'),
 path('failure/failure-<int:comment_id>-comment', views.failure_comment, name='failure_comment'),
 path('company-list', views.CompanyList.as_view(), name='company_list'),
 path('company-<slug:pk>-info', views.CompanyDetail.as_view(), name='company_info'),
]