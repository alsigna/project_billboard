from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from board.models import Author, Category, Comment, Post


class PostAdminForm(forms.ModelForm):
    title = forms.CharField(
        label="Заголовок",
    )
    content = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Сообщение",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        label="Категория",
    )
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        empty_label=None,
        label="Автор",
    )

    class Meta:
        model = Post
        fields = ("title", "author", "category", "content")


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
