from django.db import models
from django.conf import settings
# Create your models here.
class Comment(models.Model):

	user = models.ForeignKey(on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL,related_name='user')
	recipient_user = models.ForeignKey(related_name='recipient_user',on_delete=models.CASCADE,to=settings.AUTH_USER_MODEL)
	comment_text = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	accept=models.BooleanField(blank=True,default=False)
	hide=models.BooleanField(blank=True,default=False)
	def __str__(self):
		return f"пользователь: {self.user}, дата: {self.date}"

	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'