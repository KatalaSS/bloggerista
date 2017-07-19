from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify


class ProfileManager(models.Manager):
    use_for_related_fields = True

    def all(self):
        qs = self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self, user, to_toggle_user):
        user_profile = user.profile
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            adedd = False
        else:
            user_profile.following.add(to_toggle_user)
            adedd = True
        return adedd

    def is_following(self, user, followed_by_user):
        user_profile = user.profile
        if followed_by_user in user_profile.following.all():
            return True
        return False


def image_upload_to(instance, filename):
    name = instance.user
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "users/%s/%s" % (slug, new_filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='followed_by')
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    education = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

    objects = ProfileManager()

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_following(self):
        users = self.following.all()
        return users.exclude(username=self.user.username)

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})
