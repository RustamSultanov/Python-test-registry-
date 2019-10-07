from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django_registration.forms import RegistrationForm
from .models import Comment,Competence,UserAccept,Disputs,Company

class CommentEditForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     global user
    #     user = self.user
    #     # self.init_user = forms.ModelChoiceField(queryset=UserAccept.objects.select_related('user').filter(company=self.user.useraccept.company))
    #     super(CommentEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = [
                'verifier', 'comment_for_rating', 'comment_for_rating_competence', 'comment_for_rating_employee', 'competence','customer_flag','implementer_flag',
                'init_user','implementer','files','rating','employee','another_employee','rating_competence','rating_employee'
                 ]
        widgets = {
                'comment_for_rating': forms.Textarea(attrs={'rows' : '2'}),
                'customer_flag': forms.CheckboxInput(attrs={"class":"filled-in",}),
                'implementer_flag': forms.CheckboxInput(attrs={"class":"filled-in", }),
                # 'init_user': forms.Select(attrs={'disabled':"disabled", 'selected':"selected"})
                }

class AcceptForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [ 'accept','failure','failure_text']
        widgets = {
                'accept': forms.CheckboxInput(attrs={"class":"filled-in",}),
                'failure': forms.CheckboxInput(attrs={"class":"filled-in",}),
                'failure_text': forms.Textarea(attrs={'rows' : '2'})
                }


class CompetenceForm(forms.ModelForm):

    class Meta:
        model = Competence
        fields = [ 'competence_name']


class DisputForm(forms.ModelForm):

    class Meta:
        model = Disputs
        fields = ['text']
        widgets = {
                'text': forms.Textarea(attrs={'id' : 'textarea1','class' : 'materialize-textarea',})
                }


class RegistrationEmployeeForm(UserCreationForm):
    #password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите пароль', 'name' : 'password_check'}))
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
        'email' : forms.EmailInput(attrs={'placeholder' : 'Ваша почта'}),
        'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя', 'name' : 'Name'}),
        'last_name' : forms.TextInput(attrs={'placeholder' : 'Фамилия', 'name' : 'Surname'}),
        #'password' : forms.PasswordInput(attrs={'placeholder' : 'Пароль', 'name' : 'pass'}),
        }

        error_messages = {
            'email': {
                'max_length': ("Превышена длинна"),
            },
        }

        labels = {
            "email": "Ваша почта"
        }
        def __init__(self, *args, **kwargs):
            super(RegistrationForm, self).__init__(*args, **kwargs)
'''
    def clean(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        password_check = self.cleaned_data['password_check']
        password = self.cleaned_data['password']
        if password_check!=password:
            raise forms.ValidationError('Пароль не совпадает!')
 '''       
class CheckCompanyForm(forms.Form):
    
    TIN_or_PSRN = forms.IntegerField(label='ИНН/ОГРН', help_text='ИНН содержит 10 чисел, ОГРН - 13 чисел')

    def clean_TIN_or_PSRN(self):
        TIN_or_PSRN = self.cleaned_data['TIN_or_PSRN']
        length_number = len(str(TIN_or_PSRN))
        print(length_number)
        if length_number != 10 and length_number != 13:
            print('Ошибка')
            raise forms.ValidationError('Неверное количество чисел')

class InvitationForm(forms.Form):

    email = forms.EmailField(label='E-mail Получателя приглашения')

class EditCompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ['logo', 'competence', 'description']


class RegistrationAceptUserForm(forms.ModelForm):

    class Meta:
        model = UserAccept
        fields = ['city', 'userpic', 'biography', 'contacts']