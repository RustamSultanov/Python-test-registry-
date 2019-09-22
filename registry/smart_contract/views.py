from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CommentEditForm, AcceptForm, CompetenceForm, RegistrationEmployeeForm, DisputForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
import os


def save_comment_form(new_comment, adition_user, employee, competence,
                      another_employee):
    new_comment.save()
    for user in adition_user:
        new_comment.recipient_user.add(user)
    for user in employee:
        new_comment.employee.add(user)
    for user in competence:
        new_comment.competence.add(user)
    for user in another_employee:
        new_comment.another_employee.add(user)
    for user in another_employee:
        new_comment.recipient_user.add(user)
    for user in employee:
        new_comment.recipient_user.add(user)


# Create your views here.

def base(request):
    return render(request, 'index.html', )


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
    """Список коллег"""
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
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if new_comment.implementer_flag:
            new_comment.implementer = request.user
            new_comment.customer = form.cleaned_data['implementer']
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment, adition_user=adition_user,
                              employee=employee, competence=competence, another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        if new_comment.customer_flag:
            new_comment.implementer = form.cleaned_data['implementer']
            new_comment.customer = request.user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment, adition_user=adition_user,
                              employee=employee, competence=competence, another_employee=another_employee)
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
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if new_comment.implementer_flag:
            new_comment.implementer = request.user
            new_comment.customer = form.cleaned_data['implementer']
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment, adition_user=adition_user,
                              employee=employee, competence=competence, another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        if new_comment.customer_flag:
            new_comment.implementer = form.cleaned_data['implementer']
            new_comment.customer = request.user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment, adition_user=adition_user,
                              employee=employee, competence=competence, another_employee=another_employee)
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


@login_required
def accept_comment(request, comment_id):
    """Верификация комментария"""
    user = request.user
    comment = Comment.objects.get(recipient_user=request.user.id, id=comment_id, accept=False)
    disputs = Disputs.objects.select_related('user', 'comment').filter(comment=comment_id)
    form1 = DisputForm(request.POST or None)
    if form1.is_valid():
        new_disput = form1.save(commit=False)
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '#comments')
    form = AcceptForm(request.POST or None, instance=comment)
    if form.is_valid():
        new_accept = form.save(commit=False)
        accept = form.cleaned_data['accept']
        failure = form.cleaned_data['failure']
        if failure:
            return HttpResponseRedirect(reverse('failure_comment', args=[comment_id]))
        if accept:
            user = User.objects.get(id=request.user.id)
            user.useraccept.accept = True
            user.useraccept.save()
            for user in comment.recipient_user.all():
                users = User.objects.get(id=user.id)
                if not users.useraccept.accept:
                    print("Fail!")
                    break
            else:
                new_accept.accept = accept
                recipient_users = ''
                for user in comment.recipient_user.all():
                    recipient_users += (user.last_name + user.first_name + user.useraccept.company + ',')
                    user = User.objects.get(id=user.id)
                    user.useraccept.accept = False
                    user.useraccept.save()
                data_comment = f'''"
                    Status - accepted, user - {comment.user}, recipient_users - {recipient_users}, 
                    comment - {comment.comment_text}"'''
                command = r'''curl -H "Content-type:application/json" --data '{"data":''' + data_comment + r'''}' http://localhost:3001/mineBlock'''
                print(data_comment, command)
                os.system(command)
                new_accept.save()
                return HttpResponseRedirect(reverse_lazy('comment_list'))
            return HttpResponseRedirect(reverse_lazy('comment_list'))
        return HttpResponseRedirect(reverse_lazy('comment_list'))
    return render(request, 'accept_form.html',
                  {'form': form, 'form1': form1, 'disputs': disputs, 'comment': comment})


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
            recipient_users = ''
            for user in comment.recipient_user.all():
                recipient_users += (user.last_name + user.first_name + user.useraccept.company + ',')
                user = User.objects.get(id=user.id)
                user.useraccept.failure = False
                user.useraccept.save()
            data_comment = f'''"
                Status - failure, user - {comment.user}, recipient_users - {recipient_users}, comment - {comment.comment_text}, 
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
    return render(request, 'user.html', {'user': user,
                                         'verify_count': verify_count})


def show_genres(request):
    return render(request, "genre.html", {'genres': Competence.objects.all()})
