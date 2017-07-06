from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.generic import RedirectView, ListView

from .forms import PostForm
from .models import Post
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


def create(request):
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
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/detail.html', {'post': post})


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


# cbv for post_like_toggle function
class PostLikeToggle(RedirectView):
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
