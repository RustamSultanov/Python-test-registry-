from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
def get_custom_username(self):
	return f"Компания: {self.useraccept.company}, сотрудник: {self.first_name} {self.last_name}"
User.add_to_class("__str__",get_custom_username)

class UserAccept(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	accept=models.BooleanField(blank=True,default=False)
	failure=models.BooleanField(blank=True,default=False)
	company = models.CharField(max_length=100)
	position = models.CharField(max_length=100)
	def __str__(self):
		return f"Компания: {self.company}, сотрудник: {self.user.first_name} {self.user.last_name}"



class Competence(MPTTModel):
    competence_name = models.CharField(max_length=256)
    name = models.CharField(max_length=256, unique=True,)
    owner = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f"#{self.id} {self.competence_name}; Создал: {self.owner.useraccept.company}"




class Comment(models.Model):

	user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user')
	competence = models.ManyToManyField(Competence)
	implementer = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='implementer',blank=True)
	customer = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='customer',blank=True)
	init_user = models.ForeignKey(on_delete=models.CASCADE,to=User,related_name='init_user',blank=True)
	implementer_flag = models.BooleanField(blank=True,default=False)
	customer_flag = models.BooleanField(blank=True,default=False)
	recipient_user = models.ManyToManyField(User)
	adition_user = models.ManyToManyField(User,related_name='adition_user',blank=True,)
	employee = models.ManyToManyField(User,related_name='employee_list',blank=True)
	another_employee = models.ManyToManyField(User,related_name='another_employee',blank=True)
	comment_text = models.TextField()
	date_update = models.DateTimeField(auto_now=True,blank=True,null=True)
	date_create = models.DateTimeField(auto_now_add=True)
	accept=models.BooleanField(blank=True,default=False)
	hide=models.BooleanField(blank=True,default=False)
	failure=models.BooleanField(blank=True,default=False)
	failure_text = models.TextField(blank=True,null=True)
	RATING_CHOICE = (
        (1, "Ужасно"),
        (2, "Плохо"),
        (3, "Нормально"),
        (4, "Хорошо"),
        (5, "Отлично"),
    )
	rating = models.IntegerField(choices=RATING_CHOICE, default=4)
	rating_competence = models.IntegerField(choices=RATING_CHOICE, default=4)
	rating_employee = models.IntegerField(choices=RATING_CHOICE, default=4)
	files = models.FileField(upload_to='prod_doc',blank=True)
	def __str__(self):
		return f"автор: {self.user}, дата: {self.date_create}"

	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'


class Disputs(models.Model):

	user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user_disput')
	comment = models.ForeignKey(on_delete=models.CASCADE,to=Comment,related_name='comment')
	text = models.TextField()
	date_create = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.comment}"

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'