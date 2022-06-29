from django.urls import path

from .views import CommentList, PostCreate, PostDelete, PostEdit, PostList

app_name = "board"

urlpatterns = [
    path("", PostList.as_view(), name="post_list"),
    path("new", PostCreate.as_view(), name="post_add"),
    path("comments", CommentList.as_view(), name="comment_list"),
    path("<int:pk>/edit", PostEdit.as_view(), name="post_edit"),
    path("<int:pk>/delete", PostDelete.as_view(), name="post_delete"),
]
