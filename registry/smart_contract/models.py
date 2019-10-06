from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Competence(MPTTModel):
    competence_name = models.CharField(max_length=256)
    name = models.CharField(max_length=256, unique=True, )
    owner = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"#{self.id} {self.competence_name}; Создал: {self.owner.useraccept.company}"

    class Meta:
        verbose_name = 'Компетенция'
        verbose_name_plural = 'Компетенции'


'''Автоматическое создание имени файла изображения'''
def image_folder(instance, filename):
	
	filename = instance.slug + '.' + filename.split('.')[1]
	return f"{instance.slug}/{filename}"

class Company(models.Model):   
    name = models.CharField(max_length=50, verbose_name='Название компании',
                            blank=True, null=True)
    legal_address = models.CharField(max_length=100, verbose_name='Юридический адресс',
                            blank=True, null=True)
    TIN = models.BigIntegerField(unique=True, verbose_name='ИНН', 
                            help_text='10 целых чисел')
    PSRN = models.BigIntegerField(unique=True, verbose_name='ОГРН', 
                            help_text='13 целых чисел')
    KPP = models.BigIntegerField(unique=True, verbose_name='КПП', 
                            help_text='9 целых чисел')
    CEO = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to=image_folder, 
                            verbose_name='Логотип', blank=True, null=True)
    competence = models.ManyToManyField(Competence, verbose_name='Компетенции компании', blank=True)
    description = models.TextField(verbose_name='О компании', blank=True)

    def __str__(self):
        return f"Компания: {self.name}"

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


# User.add_to_class("__str__", get_custom_username)
def get_custom_username(self):
    return f"Компания: {self.useraccept.company}, сотрудник: {self.first_name} {self.last_name}"

class UserAccept(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, verbose_name='Город проживания', default='Москва')
    userpic = models.ImageField(upload_to=image_folder, 
                            verbose_name='Юзерпик', blank=True, null=True)
    biography = models.TextField(verbose_name='Краткая биография', blank=True)
    contacts = models.TextField(verbose_name='Контакты', blank=True)                    
    accept = models.BooleanField(blank=True, default=False)
    failure = models.BooleanField(blank=True, default=False)
    company = models.CharField(max_length=100)
    company_test = models.ForeignKey(Company, models.SET_NULL, blank=True, null=True)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"Компания: {self.company}, сотрудник: {self.user.first_name} {self.user.last_name}"


class Comment(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='user')
    competence = models.ManyToManyField(Competence)
    implementer = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='implementer',
                                    blank=True)
    customer = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='customer',
                                 blank=True)
    init_user = models.ForeignKey(on_delete=models.CASCADE, to=User, related_name='init_user', blank=True)
    implementer_flag = models.BooleanField(blank=True, default=False)
    customer_flag = models.BooleanField(blank=True, default=False)
    recipient_user = models.ManyToManyField(User)
    verifier = models.ManyToManyField(User, related_name='verifier', blank=True)
    employee = models.ManyToManyField(User, related_name='employee_list', blank=True)
    another_employee = models.ManyToManyField(User, related_name='another_employee', blank=True)    
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(blank=True, default=False)
    hide = models.BooleanField(blank=True, default=False)
    failure = models.BooleanField(blank=True, default=False)
    failure_text = models.TextField(blank=True, null=True)
    RATING_CHOICE = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )
    rating = models.IntegerField(choices=RATING_CHOICE, default=4)
    comment_for_rating = models.TextField(verbose_name='Пояснение к общей оценке', blank=True)
    rating_competence = models.IntegerField(choices=RATING_CHOICE, default=4)
    comment_for_rating_competence = models.TextField(verbose_name='Пояснение к оценке компетенции', blank=True)
    rating_employee = models.IntegerField(choices=RATING_CHOICE, default=4)
    comment_for_rating_employee = models.TextField(verbose_name='Пояснение к оценке сотрудника', blank=True)
    files = models.FileField(upload_to='prod_doc', blank=True)

    def __str__(self):
        return f"автор: {self.user}, дата: {self.date_create}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Disputs(models.Model):
    user = models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL, related_name='user_disput')
    comment = models.ForeignKey(on_delete=models.CASCADE, to=Comment, related_name='comment')
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'