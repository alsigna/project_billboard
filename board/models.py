from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    subscribers = models.ManyToManyField(Author, related_name="categories", blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def get_absolute_url(self) -> str:
        return reverse("board:post_edit", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        if len(self.title) > 32:
            return self.title[:32] + "..."
        else:
            return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_ack = models.BooleanField(default=False)
