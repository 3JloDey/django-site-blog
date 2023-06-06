from typing import Any

from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_queryset(self) -> QuerySet[Any]:
        return Post.published.all()

    def get_object(self, queryset=None) -> Any:
        print(self.kwargs)
        year, month, day, post_slug = (
            self.kwargs.get("year"),
            self.kwargs.get("month"),
            self.kwargs.get("day"),
            self.kwargs.get("post"),
        )
        queryset = queryset or self.get_queryset()
        return get_object_or_404(
            queryset,
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post_slug,
        )


def post_share(request, post_id) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
            message = f"Прочитай {post.title} по ссылке {post_url}\n\n{cd['name']} прокомментировал: {cd['comments']}"
            send_mail(subject, message, "your_account@gmail.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
