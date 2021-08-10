from django import forms

from .models import Post, Comment, Tag

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'cover', 'attachment', 'tags', )



    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Criar', css_class='btn-lg save'))

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Comentar', css_class='btn-lg save'))


class TagForm(forms.ModelForm):
    choices = [(post.pk, post.title) for post in Post.objects.all()]
    posts = forms.MultipleChoiceField(
        required=False,
        choices=choices

    )

    class Meta:
        model = Tag
        fields = ('name', 'posts', )

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Salvar', css_class='btn-lg save'))