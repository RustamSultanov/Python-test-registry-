from .models import Comment

def comment_counter(user):
    return Comment.objects.filter(user=user.id).count() + Comment.objects.filter(recipient_user=user.id).count()

def count_comments_and_accepts(request):
    user = request.user
    comment_count = comment_counter(user=user)
    accept_count = Comment.objects.filter(recipient_user=user.id, accept=False, failure=False).count()
    context = {
        'comment_count': comment_count, 
        'accept_count': accept_count
    }
    return context