from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .forms import CommentEditForm,AcceptForm,CompetenceForm,RegistrationEmployeeForm,DisputForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.db.models import Count
import os

def save_comment_form(new_comment,comment_text,files,rating,init_user,adition_user,employee,competence,another_employee):
    new_comment.comment_text = comment_text
    new_comment.files = files
    new_comment.rating = rating
    new_comment.init_user = init_user
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

def comment_counter(user):
    return Comment.objects.filter(user=user.id).count() + Comment.objects.filter(recipient_user=user.id).count()

# Create your views here.

def base(request):
    return render(request, 'index.html',)

@login_required
def registration_view(request):
    form = RegistrationEmployeeForm(request.POST or None,auto_id=False)
    if form.is_valid():
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user = request.user
        email=form.cleaned_data['username']
        new_user.email = email
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()
        user_company=UserAccept(user=User.objects.get(id = new_user.id),company=user.useraccept.company)
        user_company.save()
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    context = {
        'form': form
    }
    return render(request, 'register_form.html', context)

@login_required
def employee_list(request):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    employee_list = UserAccept.objects.select_related('user').filter(company=user.useraccept.company)
    return render(request, 'lk_employee.html',{'employee_list':employee_list,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def lichniy_kabinet(request):
    user = request.user
    comment_list_in = Comment.objects.prefetch_related('user','competence').filter(user=user.id)
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment_list_out = Comment.objects.prefetch_related('user','competence').filter(recipient_user=user.id)
    context = {
    'comment_list_in':comment_list_in,
    'comment_list_out':comment_list_out,
    'comment_count':comment_count,
    'accept_count':accept_count
    }
    return render(request, 'lk_comment_list.html', context)

@login_required
def competence_list(request):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    competence_list=Competence.objects.all()
    form = CompetenceForm(request.POST or None)
    if form.is_valid():
        new_competence = form.save(commit=False)
        competence_name = form.cleaned_data['competence_name']
        new_competence.competence_name = competence_name
        new_competence.owner=request.user
        new_competence.save()
        return HttpResponseRedirect(reverse('competence_list'))
    return render(request, 'competence_form.html',{'form': form,'competence_list':competence_list,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def delete_comment(request, comment_id):
    author_id = request.user
    Comment.objects.get(user=author_id,id=comment_id,accept=False).delete()
    return HttpResponseRedirect(reverse('lichniy-kabinet'))

@login_required
def lk_comment(request, comment_id):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(user=user.id,id=comment_id)
    form = CommentEditForm(request.POST or None, request.FILES or None, initial=model_to_dict(comment), instance=comment)
    if form.is_valid():
        new_comment = form.save(commit=False)
        implementer_flag = form.cleaned_data['implementer_flag']
        customer_flag = form.cleaned_data['customer_flag']
        implementer = form.cleaned_data['implementer']
        init_user = form.cleaned_data['init_user']
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        rating = form.cleaned_data['rating']
        files = form.cleaned_data['files']
        comment_text = form.cleaned_data['comment_text']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if implementer_flag == True:
            new_comment.implementer = init_user
            new_comment.customer = implementer
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))    
        if customer_flag == True:
            new_comment.implementer = implementer
            new_comment.customer = init_user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})
    return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def add_comment(request):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    form = CommentEditForm(request.POST or None, request.FILES or None, auto_id=False)
    if form.is_valid():
        new_comment = form.save(commit=False)
        implementer_flag = form.cleaned_data['implementer_flag']
        customer_flag = form.cleaned_data['customer_flag']
        implementer = form.cleaned_data['implementer']
        init_user = request.user
        competence = form.cleaned_data['competence']
        employee = form.cleaned_data['employee']
        rating = form.cleaned_data['rating']
        files = form.cleaned_data['files']
        comment_text = form.cleaned_data['comment_text']
        adition_user = form.cleaned_data['adition_user']
        another_employee = form.cleaned_data['another_employee']
        if implementer_flag == True:
            new_comment.implementer = init_user
            new_comment.customer = implementer
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))    
        if customer_flag == True:
            new_comment.implementer = implementer
            new_comment.customer = init_user
            new_comment.user = request.user
            save_comment_form(new_comment=new_comment,comment_text=comment_text,files=files,rating=rating,
            	              init_user=init_user,adition_user=adition_user,
            	              employee=employee,competence=competence,another_employee=another_employee)
            form.save_m2m()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})
    return render(request, 'add-reviews.html', {'form': form,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def lk_accept(request):
    user = request.user
    comment_list = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).select_related('user')
    comment_count = comment_counter(user=user) 
    accept_count = Comment.objects.filter(recipient_user=request.user.id,accept=False,failure=False).count()
    return render(request, 'lk_accept.html',{'comment_list':comment_list,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def accept_comment(request, comment_id):
    user = request.user
    comment_count = comment_counter(user=user) 
    accept_count = Comment.objects.filter(recipient_user=request.user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(recipient_user=request.user.id,id=comment_id,accept=False)
    disputs = Disputs.objects.filter(comment=comment_id)
    form1 = DisputForm(request.POST or None)
    if form1.is_valid():
        new_disput = form1.save(commit=False)
        text = form1.cleaned_data['text']
        new_disput.text = text
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(f'../lk-accept/accept-{comment_id}-comment#comments')
    form = AcceptForm(request.POST or None,instance=comment)
    if form.is_valid():
        new_accept = form.save(commit=False)
        accept = form.cleaned_data['accept']
        failure = form.cleaned_data['failure']
        if failure == True:
        	return HttpResponseRedirect(f'../lk-failure/failure-{comment_id}-comment')
        if accept == True:
            user=User.objects.get(id=request.user.id)
            user.useraccept.accept=True
            user.useraccept.save()
            for user in comment.recipient_user.all():
                users=User.objects.get(id=user.id)
                if users.useraccept.accept == False:
                    print("Fail!")
                    break
            else:
                new_accept.accept = accept
                recipient_users=''
                for user in comment.recipient_user.all():
                    recipient_users+=(user.last_name + user.first_name + user.useraccept.company +',')
                    user=User.objects.get(id=user.id)
                    user.useraccept.accept=False
                    user.useraccept.save()
                data_comment=f'''"
                    Status - accepted, user - {comment.user}, recipient_users - {recipient_users}, 
                    comment - {comment.comment_text}"'''
                command=r'''curl -H "Content-type:application/json" --data '{"data":'''+data_comment+r'''}' http://localhost:3001/mineBlock'''
                print(data_comment,command)
                os.system(command)
                new_accept.save()
                return HttpResponseRedirect(reverse('lichniy-kabinet'))
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'accept_form.html', {'form': form,'form1':form1,'disputs':disputs,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})


@login_required
def lk_failure(request,comment_id):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    comment = Comment.objects.get(recipient_user=user.id,id=comment_id,failure=False)
    form = AcceptForm(request.POST or None,initial=model_to_dict(comment),instance=comment)
    if form.is_valid():
        new_failure = form.save(commit=False)
        failure_text = form.cleaned_data['failure_text']
        new_failure.failure_text = failure_text
        new_failure.save()
        user=User.objects.get(id=request.user.id)
        user.useraccept.failure=True
        user.useraccept.save()
        for user in comment.recipient_user.all():
            users=User.objects.get(id=user.id)
            if users.useraccept.failure == False:
                break
        else:
            new_failure.failure=True
            recipient_users=''
            for user in comment.recipient_user.all():
                recipient_users+=(user.last_name + user.first_name + user.useraccept.company +',')
                user=User.objects.get(id=user.id)
                user.useraccept.failure=False
                user.useraccept.save()
            data_comment=f'''"
                Status - failure, user - {comment.user}, recipient_users - {recipient_users}, comment - {comment.comment_text}, 
                reason - {failure_text}"'''
            command=r'''curl -H "Content-type:application/json" --data '{"data":'''+data_comment+r'''}' http://localhost:3001/mineBlock'''
            os.system(command)
            new_failure.save()
            return HttpResponseRedirect(reverse('lichniy-kabinet'))
        return HttpResponseRedirect(reverse('lichniy-kabinet'))
    return render(request, 'failure_form.html', {'form': form,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def comment_info(request, comment_id):
    user=request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    disputs = Disputs.objects.filter(comment=comment_id)
    comment = Comment.objects.get(id=comment_id)
    form = DisputForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = user
        new_disput.comment = comment
        new_disput.save()
        return HttpResponseRedirect(f'../lk-accepted-list/info-{comment_id}-comment#comments')
    return render(request, 'comment_info.html', {'form': form,'disputs':disputs,'comment':comment,'comment_count':comment_count,'accept_count':accept_count})

@login_required
def employee_info(request, user_id):
    user = User.objects.get(id=user_id)
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id,accept=False,failure=False).count()
    verify_count = Comment.objects.filter(recipient_user=user.id,accept=True).count() + Comment.objects.filter(user=user.id,accept=True).count() 
    return render(request, 'user.html', {'user':user,'comment_count':comment_count,'accept_count':accept_count,'verify_count':verify_count})

def show_genres(request):
    return render(request, "genre.html", {'genres': Competence.objects.all()})