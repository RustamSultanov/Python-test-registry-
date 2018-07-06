from django import forms
from django.contrib.auth.models import User
from .models import Comment
from django.db import models

class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['recipient_user', 'comment_text',]
        widgets = {
                
                'comment_text': forms.Textarea(attrs={'rows' : '2'})
                }

class AcceptForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [ 'accept']
        widgets = {
                
                'accept': forms.CheckboxInput()
                }