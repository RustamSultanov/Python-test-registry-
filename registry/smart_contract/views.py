import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core import signing
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.conf import settings as django_settings
import requests
from django_registration import signals
from django_registration.views import RegistrationView as BaseRegistrationView
from registry import settings
from .models import *
from .forms import CommentEditForm, AcceptForm, CompetenceForm, RegistrationEmployeeForm, DisputForm, CheckCompanyForm, \
    InvitationCompanyForm, EditCompanyForm, RegistrationAceptUserForm


def save_comment_form(new_comment):
    new_comment.save()
    for user in new_comment.verifier:
        new_comment.recipient_user.add(user)
    for user in new_comment.employee:
        new_comment.employee.add(user)
    for user in new_comment.competence:
        new_comment.competence.add(user)
    for user in new_comment.another_employee:
        new_comment.another_employee.add(user)
    for user in new_comment.another_employee:
        new_comment.recipient_user.add(user)
    for user in new_comment.employee:
        new_comment.recipient_user.add(user)


# Create your views here.
REGISTRATION_SALT = getattr(django_settings, 'REGISTRATION_SALT', 'registration')


class RegistrationUser(BaseRegistrationView):
    email_body_template = 'django_registration/activation_email_body.txt'
    email_subject_template = 'django_registration/activation_email_subject.txt'
    success_url = reverse_lazy('django_registration_complete')   
    
    def register(self, form):
        new_user = self._create_inactive_user(form)
        signals.user_registered.send(
            sender=self.__class__,
            user=new_user,
            request=self.request
        )
        return new_user

    def _create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save(commit=False)
        new_user.username = form.cleaned_data['email'] #Email служит логином при входе, но само поле username в форме не заполняется
        new_user.is_active = False
        new_user.save()

        self._send_activation_email(new_user)

        return new_user

    @staticmethod
    def _get_activation_key(user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(
            obj=user.get_username(),
            salt=REGISTRATION_SALT
        )

    def _get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """
        protocol = 'https' if self.request.is_secure() else 'http'
        return {
            'protocol': protocol,
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request)
        }

    def _send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.

        """
        activation_key = self._get_activation_key(user)
        context = self._get_email_context(activation_key)
        context['user'] = user
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request
        )
        # Force subject to a single line to avoid header-injection
        # issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request
        )
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


class RegistrationCompany(FormView):
    '''Делает запрос в API DaData.ru, если данные из формы верные, создаёт Компанию и отправляет её данные в шаблон'''
    form_class = CheckCompanyForm
    template_name = 'check_company_form.html'

    def form_valid(self, form):
        json_response = self._request_to_API(self.request.POST['TIN_or_PSRN'])
        if json_response['suggestions']:  # Если ответ не пустой
            company, created = self._get_or_create_from_json(json_file=json_response)
            # чтобы позже прикрепить к зарегистрированному пользователю
            self.request.session['company_id'] = company.id
            return render(self.request, 'company_registration_info.html', {'company': company})
        else:
            return render(self.request, self.template_name,
                          {'form': form, 'error': 'Такая компания не зарегистрирована, пожалуйста проверьте ИНН/ОГРН'})

    @staticmethod
    def _request_to_API(TIN_or_PSRN):
        '''More info about used API https://dadata.ru/api/find-party'''
        url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': 'Token 77e78f4862b3d616275575a90de5689862fac8d8'}
        data = '{"query": "value"}'.replace("value", str(TIN_or_PSRN))
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    @staticmethod
    def _get_or_create_from_json(json_file):
        new_company, created = Company.objects.get_or_create(
            name=json_file['suggestions'][0]['value'],
            legal_address=json_file['suggestions'][0]['data']['address']["unrestricted_value"],
            TIN=json_file['suggestions'][0]['data']['inn'],
            PSRN=json_file['suggestions'][0]['data']['ogrn'],
            KPP=json_file['suggestions'][0]['data']['kpp'],
            CEO=json_file['suggestions'][0]['data']['management']['name']
        )
        return new_company, created


class RegistrationAcceptUser(FormView):
    template_name = 'django_registration/registration_acceptuser_form.html'

    form_class = RegistrationAceptUserForm
    success_url = reverse_lazy('successe_registration')

    def form_valid(self, form):
        user = self.request.user
        company = Company.objects.get(id=self.request.session['company_id'])
        useraccept = user.useraccept
        useraccept.city = form.cleaned_data['city']
        useraccept.userpic = form.cleaned_data['userpic']
        useraccept.biography = form.cleaned_data['biography']
        useraccept.contacts = form.cleaned_data['contacts']
        useraccept.company = company.name
        useraccept.company_test = company
        useraccept.save()
        return super(RegistrationAcceptUser, self).form_valid(form)


class EditCompany(FormView):
    template_name = 'company_edit_form.html'
    form_class = EditCompanyForm
    success_url = reverse_lazy('edit_company')

    def form_valid(self, form):
        return super(InvitationCompany, self).form_valid(form)


class CheckCompanyBeforeComment(FormView):
    '''Проверяет зарегистрирована ли компания в приложении по ИНН или ОГРН'''
    template_name = 'check_company_form.html'
    form_class = CheckCompanyForm

    def form_valid(self, form):
        length_number = len(str(self.request.POST['TIN_or_PSRN']))
        if length_number == 10:
            try:
                company = Company.objects.get(TIN=self.request.POST['TIN_or_PSRN'])
                return HttpResponseRedirect(reverse_lazy('add_comment'))
            except Company.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('invitation_company'))
        elif length_number == 13:
            try:
                company = Company.objects.get(PSRN=self.request.POST['TIN_or_PSRN'])
                return HttpResponseRedirect(reverse_lazy('add_comment'))
            except Company.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('invitation_company'))


class InvitationCompany(FormView):
    '''Отправляет письмо преставителю компании с приглашением зарегистрироваться в приложении'''
    template_name = 'invitation_company_form.html'
    email_subject_template = 'invitation_mail/invitation_email_subject.txt'
    email_body_template = 'invitation_mail/invitation_email_body.txt'
    form_class = InvitationCompanyForm
    success_url = reverse_lazy('success_send_invitation')

    def form_valid(self, form):
        send_to = form.cleaned_data['email']
        user = self.request.user
        protocol = 'https' if self.request.is_secure() else 'http'
        context = {
            'protocol': protocol,
            'site': get_current_site(self.request),
            'user': user
        }
        subject = render_to_string(
            template_name=self.email_subject_template,
            context=context,
            request=self.request
        )
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            template_name=self.email_body_template,
            context=context,
            request=self.request
        )
        send_mail(subject, message,
                  settings.EMAIL_HOST_USER, [send_to], fail_silently=False)
        return super(InvitationCompany, self).form_valid(form)


class CompanyDetail(DetailView):
    model = Company
    template_name = 'company_info.html'
    context_object_name = 'company'


class CompanyList(ListView):
    model = Company
    template_name = 'company_list.html'


@login_required
def registration_view(request):
    """Аутентифицированные админы регистрируют пользователей сети"""
    user = request.user
    form = RegistrationEmployeeForm(request.POST or None, auto_id=False)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        user_company = UserAccept(user=new_user, company=user.useraccept.company)
        user_company.save()
        return HttpResponseRedirect(reverse_lazy('comment_list'))
    context = {
        'form': form
    }
    return render(request, 'register_form.html', context)


@login_required
def employee_list(request):
    """Список сотрудников"""
    user = request.user
    employee_list = UserAccept.objects.select_related('user').filter(company=user.useraccept.company)
    return render(request, 'employee_list.html',
                  {'employee_list': employee_list})


@login_required
def comment_list(request):
    """Список моих отзывов"""
    user = request.user
    comment_list_in = Comment.objects.prefetch_related('user', 'competence').filter(user=user.id)
    comment_list_out = Comment.objects.prefetch_related('user', 'competence').filter(recipient_user=user.id)
    context = {
        'comment_list_in': comment_list_in,
        'comment_list_out': comment_list_out
    }
    for comment in comment_list_in:
        print(comment.rating)
    return render(request, 'comment_list.html', context)


@login_required
def competence_list(request):
    """Справочник всех компетенций"""
    competence_list_ = Competence.objects.all()
    form = CompetenceForm(request.POST or None)
    if form.is_valid():
        new_competence = form.save(commit=False)
        new_competence.owner = request.user
        new_competence.save()
        return HttpResponseRedirect(reverse_lazy('competence_list'))
    return render(request, 'competence_form.html',
                  {'form': form, 'competence_list': competence_list_})


@login_required
def delete_comment(request, comment_id):
    author_id = request.user
    Comment.objects.get(user=author_id, id=comment_id, accept=False).delete()
    return HttpResponseRedirect(reverse_lazy('comment_list'))


@login_required
def edit_comment(request, comment_id):
    """Редактирование отзывов"""
    user = request.user
    comment = Comment.objects.get(user=user.id, id=comment_id)
    form = CommentEditForm(request.POST or None, request.FILES or None, initial=model_to_dict(comment),
                           instance=comment)
    if form.is_valid():
        new_comment = form.save(commit=False)
        if new_comment.implementer_flag:
            new_comment.implementer = request.user
            new_comment.customer = form.cleaned_data['implementer']
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        if new_comment.customer_flag:
            new_comment.implementer = form.cleaned_data['implementer']
            new_comment.customer = request.user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        return render(request, 'add-reviews.html',
                      {'form': form})
    return render(request, 'add-reviews.html',
                  {'form': form})


@login_required
def add_comment(request):
    """Добавление комментария"""
    form = CommentEditForm(request.POST or None, request.FILES or None, auto_id=False)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        if new_comment.implementer_flag:
            new_comment.implementer = request.user
            new_comment.customer = form.cleaned_data['implementer']
            save_comment_form(new_comment=new_comment)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        if new_comment.customer_flag:
            new_comment.implementer = form.cleaned_data['implementer']
            new_comment.customer = request.user
            save_comment_form(new_comment=new_comment)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        return render(request, 'add-reviews.html',
                      {'form': form})
    return render(request, 'add-reviews.html',
                  {'form': form})


@login_required
def accept_list(request):
    """Список ожидающих верификации комментариев"""
    user = request.user
    comment_list_ = Comment.objects.select_related('user').filter(recipient_user=user.id, accept=False, failure=False)
    return render(request, 'accept_list.html',
                  {'comment_list': comment_list_})


def construct_message(comment):
    recipient_users = ''
    for user in comment.recipient_user.all():
        recipient_users += (user.last_name + user.first_name + user.useraccept.company + ',')
        user = User.objects.get(id=user.id)
        user.useraccept.accept = False
        user.useraccept.save()
    return recipient_users


@login_required
def accept_comment(request, comment_id):
    """Верификация комментария"""
    user = request.user
    comment = Comment.objects.get(recipient_user=request.user.id, id=comment_id, accept=False)
    disputs = Disputs.objects.select_related('user', 'comment').filter(comment=comment_id)
    disput_form = DisputForm(request.POST or None)
    if disput_form.is_valid():
        new_disput = disput_form.save(commit=False)
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '#comments')
    form = AcceptForm(request.POST or None, instance=comment)
    if form.is_valid():
        new_accept = form.save(commit=False)
        if new_accept.failure:
            return HttpResponseRedirect(reverse('failure_comment', args=[comment_id]))
        if new_accept.accept:
            user = User.objects.get(id=request.user.id)
            user.useraccept.accept = True
            user.useraccept.save()
            for user in comment.recipient_user.all():
                users = User.objects.get(id=user.id)
                if not users.useraccept.accept:
                    print("Fail!")
                    break
            else:
                recipient_users = construct_message(comment)
                data_comment = f'''"
                    Status - accepted, user - {comment.user}, recipient_users - {recipient_users}, 
                    comment - {comment.comment_for_rating}"'''
                command = r'''curl -H "Content-type:application/json" --data '{"data":''' + data_comment + r'''}' http://localhost:3001/mineBlock'''
                print(data_comment, command)
                os.system(command)
                new_accept.save()
                return HttpResponseRedirect(reverse_lazy('comment_list'))
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        return HttpResponseRedirect(reverse_lazy('comment_list'))
    return render(request, 'accept_form.html',
                  {'form': form, 'disput_form': disput_form, 'disputs': disputs, 'comment': comment})


@login_required
def failure_comment(request, comment_id):
    """Отклоняет отзыв с указанием причины"""
    user = request.user
    comment = Comment.objects.get(recipient_user=user.id, id=comment_id, failure=False)
    form = AcceptForm(request.POST or None, initial=model_to_dict(comment), instance=comment)
    if form.is_valid():
        new_failure = form.save()
        user = User.objects.get(id=request.user.id)
        user.useraccept.failure = True
        user.useraccept.save()
        for user in comment.recipient_user.all():
            users = User.objects.get(id=user.id)
            if not users.useraccept.failure:
                break
        else:
            new_failure.failure = True
            recipient_users = construct_message(comment)
            data_comment = f'''"
                Status - failure, user - {comment.user}, recipient_users - {recipient_users}, comment - {comment.comment_for_rating}, 
                reason - {new_failure.failure_text}"'''
            command = r'''curl -H "Content-type:application/json" --data '{"data":''' + data_comment + r'''}' http://localhost:3001/mineBlock'''
            os.system(command)
            new_failure.save()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        return HttpResponseRedirect(reverse_lazy('comment_list'))
    return render(request, 'failure_form.html',
                  {'form': form, 'comment': comment})


@login_required
def comment_info(request, comment_id):
    '''Информация о отзыве с возможностью обсуждения отзыва'''
    user = request.user
    disputs = Disputs.objects.select_related('user', 'comment').filter(comment=comment_id)
    comment = Comment.objects.get(id=comment_id)
    form = DisputForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#comments")
    return render(request, 'comment_info.html',
                  {'form': form, 'disputs': disputs, 'comment': comment})


@login_required
def employee_info(request, user_id):
    user = User.objects.get(id=user_id)
    verify_count = Comment.objects.filter(recipient_user=user.id, accept=True).count() + Comment.objects.filter(
        user=user.id, accept=True).count()
    return render(request, 'employee_info.html', {'user': user,
                                                  'verify_count': verify_count})
