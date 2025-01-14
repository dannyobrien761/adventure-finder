from . import views
from django.urls import path


urlpatterns = [
    path('', views.post_list, name='home'),
    path("about/", views.about_me, name="about"),
    path('<slug:slug>/', views.post_detail, name='post_detail'),# Detail view for individual posts
    path('<slug:slug>/edit_comment/<int:comment_id>',views.comment_edit, name='comment_edit'),
]