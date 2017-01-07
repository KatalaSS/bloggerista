from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .forms import PostForm
from .models import Post
from actions.utils import create_action


@login_required
def home(request):
    posts = Post.objects.filter(Q(author__in=request.user.profile.following.all()) | Q(author__id=request.user.id))

    template = 'posts/home.html'
    page_template = 'posts/home_ajax.html'
    if request.is_ajax():
        template = page_template
    context = {
        'posts': posts,
        'page_template': page_template,
    }
    return render(request, template, context)


def create(request):
    form = PostForm(request.POST or None, request.FILES or None)  # request.FILES         # User.post_set.all()
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
    post_id = post.id
    liked = False
    if request.session.get('has_liked_'+str(post_id), liked):
        liked = True
    return render(request, 'posts/detail.html', {
                                                 'post': post,
                                                 'liked': liked,
                                                 })


def like_count_blog(request):
    liked = False
    if request.method == "GET":
        user = request.user.username
        post_id = request.GET['post_id']
        post = Post.objects.get(id=int(post_id))
        if request.session.get('has_liked_' + post_id, liked):
            if post.likes > 0:
                likes = post.likes - 1
                try:
                    del request.session['has_liked_' + post_id]
                except KeyError:
                    print KeyError
        else:
            request.session['has_liked_' + post_id] = True
            likes = post.likes + 1
    post.likes = likes
    post.save()
    create_action(request.user, 'likes', post)
    return HttpResponse(likes, liked)


def search(request):
    query = request.GET.get('q')
    if query is None:
        return None
        #return reverse_lazy('home')
    else:
        qs = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        context = {'posts': qs}
        return render(request, 'posts/search.html', context)




