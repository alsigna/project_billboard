from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import Category, Comment, Post


class PostEditForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(),
    )
    category = forms.ModelChoiceField(
        label="",
        queryset=Category.objects.all(),
        required=True,
    )
    content = forms.CharField(
        label="",
        widget=CKEditorUploadingWidget(),
        required=True,
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "content",
        ]


class CommentForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Ваш комментарий ..."}),
    )

    class Meta:
        model = Comment
        fields = ("text",)
