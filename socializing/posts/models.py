from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from account.models import Profile


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    profile = models.ForeignKey(Profile)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.FileField(upload_to='posts/', blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    # likes = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]

    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})

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

