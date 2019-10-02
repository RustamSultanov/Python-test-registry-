from django import forms
from django.contrib.auth.models import User
from .models import Comment,Competence,UserAccept,Disputs
from django.db import models

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
                'adition_user', 'comment_text','competence','customer_flag','implementer_flag',
                'init_user','implementer','files','rating','employee','another_employee','rating_competence','rating_employee'
                 ]
        widgets = {
                'comment_text': forms.Textarea(attrs={'rows' : '2'}),
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


class RegistrationEmployeeForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите пароль', 'name' : 'password_check'}))
    
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        widgets = {
        'username' : forms.EmailInput(attrs={'placeholder' : 'Ваша почта'}),
        'first_name' : forms.TextInput(attrs={'placeholder' : 'Имя', 'name' : 'Name'}),
        'last_name' : forms.TextInput(attrs={'placeholder' : 'Фамилия', 'name' : 'Surname'}),
        'password' : forms.PasswordInput(attrs={'placeholder' : 'Пароль', 'name' : 'pass'}),
        }

        error_messages = {
            'username': {
                'max_length': ("Превышена длинна"),
            },
        }

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        password_check = self.cleaned_data['password_check']
        password = self.cleaned_data['password']
        if password_check!=password:
            raise forms.ValidationError('Пароль не совпадает!')
        
class RegistrationCompanyForm(forms.Form):
    
    TIN_or_PSRN = forms.IntegerField(label='ИНН/ОГРН', help_text='ИНН содержит 10 чисел, ОГРН - 13 чисел')

    def clean_TIN_or_PSRN(self):
        TIN_or_PSRN = self.cleaned_data['TIN_or_PSRN']
        l = len(str(TIN_or_PSRN))
        if l != 10 and l != 13: #TODO: Костыль для проверки длины, нужно исправить
            raise forms.ValidationError('Неверное количество чисел')