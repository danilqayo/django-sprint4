from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.conf.urls.static import static
from django.conf import settings

handler404 = "core.views.page_not_found"
handler500 = "core.views.page_failure"

urlpatterns = [
    path("pages/", include("pages.urls", namespace="pages")),
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("pages:homepage"),
        ),
        name="registration",
    ),
    path("", include("blog.urls", namespace="blog")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
