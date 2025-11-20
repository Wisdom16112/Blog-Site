from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST.get('body')
            Comment.objects.create(
                post=post,
                user=request.user,
                body=body
            )
            return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments
    })

def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)

    # Only allow the owner to delete their comment
    if request.user != comment.user:
        messages.error(request, "You cannot delete someone else's comment.")
        return redirect('post_detail', slug=comment.post.slug)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('post_detail', slug=comment.post.slug)

    return render(request, 'blog/confirm_delete.html', {'comment': comment})


