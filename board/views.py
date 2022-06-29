from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from .filters import CommentFilter, PostFilter
from .forms import CommentForm, PostEditForm
from .models import Author, Comment, Post


class PostList(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        queryset = Post.objects.all()
        filterset = PostFilter(request.GET, queryset)
        return render(
            request=request,
            template_name="board/post_list.html",
            context={
                "posts": filterset.qs,
                "comment_form": CommentForm,
                "filterset": filterset,
            },
            status=200,
        )

    def post(self, request: HttpResponse) -> HttpResponse:
        if "submit_comment_form" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment: Comment = comment_form.save(commit=False)
                user = User.objects.filter(pk=request.user.pk).first()
                author = Author.objects.filter(user=user).first()
                if author is None or user is None:
                    raise Http404("Пользователь не найден")

                post_id = request.POST.get("post_id")
                if post_id is None:
                    raise Http404("Неизвестный пост")
                post = Post.objects.filter(pk=post_id).first()
                if post is None:
                    raise Http404("Пост не найден")

                comment.author = author
                comment.post = post
                comment.save()

        return redirect(reverse("board:post_list"))


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostEditForm
    model = Post
    template_name = "board/post_edit.html"
    success_url = reverse_lazy("board:post_list")


class PostCreate(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request=request,
            template_name="board/post_edit.html",
            context={"form": PostEditForm},
            status=200,
        )

    def post(self, request):
        user = User.objects.filter(pk=request.user.pk).first()
        author = Author.objects.filter(user=user).first()
        if author is None or user is None:
            raise Http404("Пользователь не найден")

        form = PostEditForm(request.POST)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = author
            post.save()
            return redirect(reverse("board:post_list"))
        else:
            return render(
                request=request,
                template_name="board/post_edit.html",
                context={"form": form},
                status=200,
            )


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "board/post_delete.html"
    success_url = reverse_lazy("board:post_list")
    context_object_name = "post"

    def get_object(self) -> Post:
        user = User.objects.filter(pk=self.request.user.pk).first()
        author = Author.objects.filter(user=user).first()
        if author is None or user is None:
            raise Http404("Пользователь не найден")

        pk = self.kwargs.get("pk")
        if not pk:
            raise Http404("Неизвестный идентификатор поста")
        obj = Post.objects.filter(author=author, pk=pk).first()
        if obj:
            return obj
        else:
            raise Http404("Пост не найден")


class CommentList(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.filter(pk=request.user.pk).first()
        author = Author.objects.filter(user=user).first()
        if author is None or user is None:
            raise Http404("Пользователь не найден")

        queryset = Comment.objects.filter(post__author=author)
        filterset = CommentFilter(author.pk, request.GET, queryset)
        return render(
            request=request,
            template_name="board/comment_list.html",
            context={
                "comments": filterset.qs,
                "filterset": filterset,
            },
            status=200,
        )

    def post(self, request):
        if "_delete" in request.POST:
            pk = request.POST.get("_delete")
            if pk:
                comment: Comment = Comment.objects.filter(pk=int(pk)).first()
                if comment:
                    comment.delete()
        elif "_ack" in request.POST:
            pk = request.POST.get("_ack")
            if pk:
                comment: Comment = Comment.objects.filter(pk=int(pk)).first()
                if comment:
                    comment.is_ack = True
                    comment.save()
        return redirect(request.get_full_path())
