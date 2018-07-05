from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def base(request):
    return render(request, 'index.html',)

@login_required
def lichniy_kabinet(request):
    comment_list = Comment.objects.filter(user=request.session['_auth_user_id'])
    return render(request, 'lk.html')

@login_required
def delete_comment(request, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return HttpResponseRedirect(reverse('lichniy-kabinet'))

@login_required
def lk_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = AdEditForm(request.POST or None, initial=model_to_dict(comment), instance=comment, auto_id=False)
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
    return render(request, 'ad_form.html', {'form': form})


