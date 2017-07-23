from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import RedirectView

from .forms import PostForm, CommentForm
from .models import Post, Comment
from actions.utils import create_action


@login_required
def home(request):
    all_posts = Post.objects.filter(
        Q(author__in=request.user.profile.following.all()) |
        Q(author__id=request.user.id))

    page = request.GET.get('page', 1)

    paginator = Paginator(all_posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    index = posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]
    template = 'posts/home.html'
    context = {
        'posts': posts,
        'page_range': page_range
    }
    return render(request, template, context)


def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.profile = request.user.profile
        instance.save()
        create_action(request.user, 'created', instance)
        return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'posts/create.html', context)


def post_detail(request, slug=None):
    """
    Display a post, its comments and create comments for that post instance
    """
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    # request.FILES or None, in case user uploads files or photos
    form = CommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.post = post
        instance.save()
        messages.success(request, 'Comment created successfully')
        return redirect(post.get_absolute_url())
    context = {
        'post': post,
        'comments': comments,
        "comment_form": form,
    }
    return render(request, 'posts/detail.html', context)


def post_update(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.user != post.author:
        messages.success(request, "You can't edit posts that aren't yours")
        return redirect(post.get_absolute_url())
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.profile = request.user.profile
        instance.save()
        messages.success(request, '{} updated successfully'.format(post))
        return redirect(post.get_absolute_url())
    context = {
        "form": form,
        'post': post,
    }
    return render(request, "posts/create.html", context)


def post_delete(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.success(request, "You can't delete posts that aren't yours")
        return redirect(post.get_absolute_url())
    return redirect("home")


def comment_delete(request, slug=None, pk=None):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        messages.success(request, "Successfully deleted")
    else:
        messages.success(request, "You can't delete comments that aren't yours")
        return redirect(post.get_absolute_url())
    return redirect(post.get_absolute_url())


def post_like_toggle(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        create_action(request.user, 'unlikes', post)
    else:
        post.likes.add(user)
        create_action(request.user, 'likes', post)
    return redirect("detail", slug=slug)


class PostLikeToggle(RedirectView):
    """
    Class Base View same as post_like_toggle function
    """
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        post = get_object_or_404(Post, slug=slug)
        url_ = post.get_absolute_url()
        user = self.request.user
        if user in post.likes.all():
            post.likes.remove(user)
            create_action(self.request.user, 'unlikes', post)
        else:
            post.likes.add(user)
            create_action(self.request.user, 'likes', post)
        return url_


def search(request):
    query = request.GET.get('q')
    if query is None:
        return None
    else:
        qs = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    context = {'posts': qs}
    return render(request, 'posts/search.html', context)
