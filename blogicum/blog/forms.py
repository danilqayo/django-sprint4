from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateInput(attrs={"type": "date"}),
        }


class CommentPostForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
