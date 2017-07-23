from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

from account.models import Profile


def image_upload_to(instance, filename):
    title = instance.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" % (slug, instance.id, file_extension)
    return "posts/%s/%s" % (slug, new_filename)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    profile = models.ForeignKey(Profile)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(upload_to=image_upload_to, blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    @property
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

    # def get_author_profile_url(self):
    #     return 'account/profile/{}'.format(self.author)

    def get_like_url(self):
        return reverse("like-toggle", kwargs={"slug": self.slug})

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Post, self).save()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    content = models.CharField(max_length=160)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(
        default='0.0.0.0', verbose_name="ip address")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             related_name='comment_user')

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ['-created']

    def user_photo(self):
        if self.user.profile.photo:
            return self.user.profile.photo.url
        else:
            return open('/static/img/avatar2.jpg').read()
