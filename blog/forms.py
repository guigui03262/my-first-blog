from django import forms

from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover', 'attachment', 'tags', )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class TagForm(forms.ModelForm):
    choices = [(post.pk, post.title) for post in Post.objects.all()]
    posts = forms.MultipleChoiceField(
        required=False,
        choices=choices

    )

    class Meta:
        model = Tag
        fields = ('name', 'posts', )
