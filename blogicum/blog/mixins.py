from django.shortcuts import redirect


class AuthorPostAccessMixin:
    """Проверяет если пользователь явялется автором поста"""

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        if self.get_object().author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
