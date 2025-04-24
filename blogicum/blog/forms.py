from django import forms

from blog.models import Comment, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CommentPostForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {"text": forms.Textarea(attrs={"cols": 10, "rows": 5})}
