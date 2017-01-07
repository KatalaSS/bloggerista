from django.forms import ModelForm, TextInput, Textarea
from .models import Post


class PostForm2(ModelForm):
    class Meta:
        model = Post
        # exclude = ['author', 'description']
        fields = ('title', 'image', )
        labels = {'title': (''), 'image': ('')}
        widgets = {'title': TextInput(attrs={'placeholder': "What's on your mind???"})}


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title',  'content', 'image',)
        labels = {'title': (''), 'image': (''), 'content': ('')}
        widgets = {'title': TextInput(attrs={'placeholder': "Enter your title"}),
                   'content': Textarea(attrs={'placeholder': "What's on your mind???"}),
                   }
        #widgets = {'title': TextInput(attrs={'placeholder': "What's on your mind???"})}



