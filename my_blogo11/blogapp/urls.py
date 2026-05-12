from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from blogapp import views

urlpatterns = [
    path("", views.post_list, name="post_list"),

    path("signup/", views.sign_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("dashboard/create-post/", views.create_post_view, name="create_post"),

    path("dashboard/edit/<int:id>/", views.edit_post, name="edit_post"),
    path("dashboard/delete/<int:id>/", views.delete_post, name="delete_post"),

    path("post/<int:id>/", views.post_detail, name="post_detail"),

    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)