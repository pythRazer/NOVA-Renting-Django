from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "nova"
urlpatterns = [
    # properties views
    # Home page for logged-in user -> dashboard, not logged in user -> ad page
    path('', views.home_page, name="home-page"),
    path('about', views.about, name="about"),
    # Item list page
    path('properties-list', views.properties_list, name="properties-list"),


    # Register (not yet implement), only has interface

    path('search-result', views.search_result, name="search-result"),

    # CRUD properties
    path('post-property-page', views.post_property_page, name="post-property-page"),
    path('<int:property_id>/delete', views.delete_property, name='delete-property'),
    path('<int:property_id>/edit', views.edit_property_page, name="edit-property-page"),
    path('<int:property_id>', views.property_detail, name="property-detail"),
    # Comment CRUD
    path('comments/post', views.post_comment, name="post-comment"),
    path('<int:property_id>/comments/<int:comment_id>/delete', views.delete_comment, name="delete-comment"),
    # path('comments/delete', views.delete_comment, name='delete-comment'),
    path('<int:property_id>/comments/<int:comment_id>/edit', views.edit_comment, name="edit-comment")
    # path('<int:property_id>/comments', views.comments, name="comments"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
