from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from actions.utils import create_action
from actions.models import Action
from posts.models import Post


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            create_action(new_user, 'has created an account')
            return render(request, 'account/register_done.html', {'new_form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


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
def notifications(request):
    actions = Action.objects.exclude(user=request.user)
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
