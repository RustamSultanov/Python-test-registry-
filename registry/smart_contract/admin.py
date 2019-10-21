from django.contrib import admin
from .models import Comment, UserAccept, Competence, Disputs, Company
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from mptt.admin import MPTTModelAdmin


class UserAcceptInline(admin.StackedInline):
    model = UserAccept
    can_delete = False
    verbose_name_plural = 'Users'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserAcceptInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Disputs)
admin.site.register(Competence,MPTTModelAdmin)
admin.site.register(Company)