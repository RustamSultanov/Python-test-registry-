from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import CommentEditForm,AcceptForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict






# Create your views here.
def base(request):
    return render(request, 'index.html',)

@login_required
def lichniy_kabinet(request):
    comment_list = Comment.objects.filter(user=request.session['_auth_user_id'])
    return render(request, 'lk_comment.html',{'comment_list':comment_list})

@login_required
def delete_comment(request, comment_id):
    author_id = request.session['_auth_user_id']
    Comment.objects.get(user=author_id,id=comment_id,accept=False).delete()
    return HttpResponseRedirect(reverse('lichniy-kabinet'))

@login_required
def lk_comment(request, comment_id):
    author_id = request.session['_auth_user_id']
    comment = Comment.objects.get(user=author_id,id=comment_id)
    form = CommentEditForm(request.POST or None, initial=model_to_dict(comment), instance=comment, auto_id=False)
    if form.is_valid():
        new_comment = form.save(commit=False)
        comment_text = form.cleaned_data['comment_text']
        author_id = User.objects.get(id = request.session['_auth_user_id'])
        recipient_user=form.cleaned_data['recipient_user']
        new_comment.user = author_id
        new_comment.comment_text = comment_text
        new_comment.recipient_user = recipient_user
        new_comment.save()
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'comment_form.html', {'form': form})

@login_required
def add_comment(request):
    form = CommentEditForm(request.POST or None, auto_id=False)
    if form.is_valid():
        new_comment = form.save(commit=False)
        comment_text = form.cleaned_data['comment_text']
        author_id = User.objects.get(id = request.session['_auth_user_id'])
        recipient_user=form.cleaned_data['recipient_user']
        new_comment.user = author_id
        new_comment.comment_text = comment_text
        new_comment.recipient_user = recipient_user
        new_comment.save()
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'comment_form.html', {'form': form})

@login_required
def lk_accept(request):
    comment_list = Comment.objects.filter(recipient_user=request.session['_auth_user_id'],accept=False)
    return render(request, 'lk_accept.html',{'comment_list':comment_list})

@login_required
def accept_comment(request, comment_id):
    comment = Comment.objects.get(recipient_user=request.session['_auth_user_id'],id=comment_id,accept=False)
    form = AcceptForm(request.POST or None,instance=comment)
    if form.is_valid():
        new_accept = form.save(commit=False)
        accept = form.cleaned_data['accept']
        new_accept.accept = accept
        new_accept.save()
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'accept_form.html', {'form': form,'comment':comment})
