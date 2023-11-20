from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
app_name = "users"
urlpatterns = [
    # properties views
    path('register', views.register, name='register'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/edit', views.edit_profile, name='edit-profile'),
    # Log in, Log out
    path('log-in', views.log_in_page, name="log-in-page"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),


]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
