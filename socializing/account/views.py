from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserEditForm, ProfileEditForm, UserCreateForm
from actions.utils import create_action
from actions.models import Action
from posts.models import Post
from django.core.urlresolvers import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect(reverse_lazy('home'))
    else:
        form = UserCreateForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return redirect('user_profile', request.user)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_profile(request, author=None):
    user2 = get_object_or_404(User, username=author)
    following = Profile.objects.is_following(request.user, user2)
    user_posts = Post.objects.filter(author__username=author)
    context = {'user2': user2, 'user_posts': user_posts, 'following': following}
    return render(request, 'account/profile.html', context)


@login_required
def user_list(request):
    people = User.objects.all()
    return render(request, 'account/user_list.html', {'people': people})


@login_required
def notifications(request, author):
    actions = Action.objects.filter(user=request.user.profile.get_following)
    actions = actions[:10]
    return render(request, 'account/notifications.html', {'actions': actions})


class UserFollowView(View):

    def get(self, request, author, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=author)
        if request.user.is_authenticated():
            is_following = Profile.objects.toggle_follow(request.user, toggle_user)
            create_action(request.user, 'follows', toggle_user)
        return redirect('user_profile', author=author)


def following(request, author):
    following = get_object_or_404(User, username=author)
    return render(request, 'account/following.html', {'following': following})


def followers(request, author):
    followers = get_object_or_404(User, username=author)
    return render(request, 'account/followers.html', {'followers': followers})
