from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.forms import CustomUserChangeForm
from .forms import PostForm, CommentForm, TagForm
from .models import Post, Comment, PostLike, PostDislike, Tag
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') 
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views +=1
    post.save()
    liked = False
    disliked = False
    if request.user.is_authenticated:
        likes_count = PostLike.objects.filter(post_id=pk, user=request.user).count()
        dislikes_count = PostDislike.objects.filter(post_id=pk, user=request.user).count()

        if likes_count == 0 and dislikes_count == 0:
            liked = False
            disliked = False

        elif likes_count == 1:
            liked = True
            disliked = False

        else:
            liked = False
            disliked = True

    
    if post.dislikes_count() == 0 and post.likes_count() == 0:
        percent = 0

    else:
        percent = (post.likes_count() / (post.dislikes_count() + post.likes_count())) * 100

    return render(request, 'blog/post_detail.html', {'post': post, 'liked': liked, 'disliked': disliked, 'percent': percent})

@login_required
def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST, request.FILES)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             form.save_m2m()
             messages.success(request, 'Critica criada com Sucesso!')
             return redirect('post_detail', pk=post.pk)
         else:
            logger.error("Erro ao criar a critica")
            messages.warning(request, 'Error! Corrija os erros abaixo.') 
     else:
         form = PostForm()
     return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, request.FILES, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             form.save_m2m()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    messages.success(request, 'Critica publicada com Sucesso!')
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    messages.success(request, 'Critica removida com Sucesso!')
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comentario adicionado com Sucesso!')
            return redirect('post_detail', pk=post.pk)
        else:
            logger.error("Erro ao criar o comentario")
            messages.warning(request, 'Error! Corrija os erros abaixo.') 
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def post_like(request, pk):
    dislikes_count = PostDislike.objects.filter(post_id=pk, user=request.user).count()

    if dislikes_count == 0:
        post_like, created = PostLike.objects.get_or_create(post_id=pk, user=request.user)
    messages.success(request, 'É like like like')
    return redirect('post_detail', pk=pk)

@login_required
def post_dislike(request, pk):
    likes_count = PostLike.objects.filter(post_id=pk, user=request.user).count()

    if likes_count == 0:
        post_dislike, created = PostDislike.objects.get_or_create(post_id=pk, user=request.user)
    messages.success(request, 'Dislike :(')
    return redirect('post_detail', pk=pk)

@login_required
def user_list(request):
    UserModel = get_user_model()
    users = UserModel.objects.all().order_by('birth_date')
    return render(request, 'blog/user_list.html', {'users': users})

@login_required
def user_remove(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    user.delete()
    messages.success(request, 'Usuario removido')
    return redirect('user_list')

@login_required
def user_edit(request, pk):
    UserModel = get_user_model()
    user = get_object_or_404(UserModel, pk=pk)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Editado')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'blog/user_edit.html', {'form': form})

@login_required
def tag_new(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            posts = form.cleaned_data['posts']
            for post in posts:
                tag.post_set.add(post)
        messages.success(request, 'Tag criada')
        return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'blog/tag_edit.html', {'form': form})

@login_required
def tag_list(request):
    tags = Tag.objects.all()

    return render(request, 'blog/tag_list.html', {'tags': tags})

def post_info(request):
    return render(request, 'blog/info.html', {})


