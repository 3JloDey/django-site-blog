# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


# region FunctionalViewPostList
# def post_list(request):
#     post_list = Post.published.all()

#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get("page", 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)

#     return render(request, "blog/post/list.html", {"posts": posts})
# endregion


class PostDetailView(View):
    def get(self, request, year, month, day, post):
        post = get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=post,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )
        return render(request, "blog/post/detail.html", {"post": post})


# region FuntionalPostDetailView
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         Post,
#         status=Post.Status.PUBLISHED,
#         slug=post,
#         publish__year=year,
#         publish__month=month,
#         publish__day=day,
#     )
#     return render(request, "blog/post/detail.html", {"post": post})
# endregion
