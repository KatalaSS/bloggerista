from django.forms import ModelForm, TextInput, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title',  'content', 'image',)
        labels = {'title': '', 'image': '', 'content': ''}
        widgets = {'title': TextInput(attrs={'placeholder': "Enter your title"}),
                   'content': Textarea(attrs={'placeholder': "What's on your mind???"}),
                   }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        labels = {'content': ''}
        widgets = {
                   'content': TextInput(attrs={'placeholder': "Write a comment here..."}),
                   }
