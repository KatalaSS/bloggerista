from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserEditForm, ProfileEditForm, UserCreateForm
from .models import Profile
from actions.utils import create_action
from actions.models import Action
from posts.models import Post

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            return redirect(reverse_lazy('home'))
    else:
        form = UserCreateForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_profile(request, author=None):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.success(request, '%s is already taken. Pick another username' % request.user)
        return redirect('edit_profile', author=request.user)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_profile(request, author=None):
    instance = get_object_or_404(User, username=author)
    following = Profile.objects.is_following(request.user, instance)
    user_posts = Post.objects.filter(author__username=author)
    context = {'instance': instance,
               'user_posts': user_posts,
               'following': following}
    return render(request, 'account/user_profile.html', context)


@login_required
def user_list(request):
    all_people = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_people, 12)
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        people = paginator.page(1)
    except EmptyPage:
        people = paginator.page(paginator.num_pages)

    index = people.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'account/user_list.html',
                  {'people': people,
                   "page_range": page_range})


@login_required
def notifications(request, author):
    all_actions = Action.objects.filter(user=request.user.profile.get_following)
    page = request.GET.get('page', 1)

    paginator = Paginator(all_actions, 10)
    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        actions = paginator.page(1)
    except EmptyPage:
        actions = paginator.page(paginator.num_pages)

    index = actions.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'account/notifications.html',
                  {'actions': actions,
                   'page_range': page_range})


def user_follow_view(request, author=None):
    toggle_user = get_object_or_404(User, username__iexact=author)
    if request.user.is_authenticated():
        is_following = Profile.objects.toggle_follow(request.user, toggle_user)
        create_action(request.user, 'follows', toggle_user)
    return redirect('user_profile', author=author)


def following(request, author):
    user = get_object_or_404(User, username=author)
    is_following = user.profile.get_following
    return render(request, 'account/is_following.html', {'is_following': is_following})


def followers(request, author):
    user = get_object_or_404(User, username=author)
    followers = user.followed_by.all
    return render(request, 'account/followers.html', {'followers': followers})
