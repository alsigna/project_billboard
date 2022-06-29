from django_filters import CharFilter, FilterSet, ModelChoiceFilter

from .models import Author, Category, Comment, Post


class CommentFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label="Автор комментария",
        empty_label="любой",
    )
    text = CharFilter(
        label="Текст комментария",
        lookup_expr="icontains",
    )
    post = ModelChoiceFilter(
        queryset=Post.objects.all(),
        label="Пост",
        empty_label="любой",
    )

    class Meta:
        model = Comment
        fields = ("author", "post", "text")

    def __init__(self, post_author_pk: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.fields["post"].queryset = Post.objects.filter(author__pk=post_author_pk)


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label="Автор поста",
        empty_label="любой",
    )
    content = CharFilter(
        label="Текст поста",
        lookup_expr="icontains",
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Категория",
        empty_label="любая",
    )

    class Meta:
        model = Comment
        fields = ("author", "content", "category")
