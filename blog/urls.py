from django.urls import path
from . import views

urlpatterns = [
    path("", views.fp.as_view(),name="firstpage"),
    path("posts", views.allp.as_view(),name="allposts"),
    path("posts/<slug:slug>", views.SinglePost.as_view(),name="detail"),
    path("read-later", views.ReadLater.as_view(), name="read-later")
]