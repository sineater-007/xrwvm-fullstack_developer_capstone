"""djangoproj URL Configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),

    path("", TemplateView.as_view(template_name="Home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="About.html"),
         name="about"),
    path("contact/", TemplateView.as_view(template_name="Contact.html"),
         name="contact"),

    path("login/", TemplateView.as_view(template_name="index.html"),
         name="login"),
    path("register/", TemplateView.as_view(template_name="index.html"),
         name="register"),
    path("dealers/", TemplateView.as_view(template_name="index.html"),
         name="dealers"),
    path("dealer/<int:dealer_id>/",
         TemplateView.as_view(template_name="index.html"),
         name="dealer-detail"),
    path("postreview/<int:dealer_id>/",
         TemplateView.as_view(template_name="index.html"),
         name="post-review"),
]

# Only serve static files via Django in development
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
