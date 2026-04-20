from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import ListView, DetailView

from blog.models import Post, Commentary


class IndexView(ListView):
    model = Post
    queryset = Post.objects.all().order_by(
        "-created_time")
    template_name = "blog/index.html"
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    queryset = Post.objects.all().prefetch_related("comments")
    template_name = "blog/post_detail.html"


class SendCommentView(LoginRequiredMixin, generic.View):
    model = Commentary
    fields = ["content"]

    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        comment = (Commentary.objects.
                   create(post=post, content=request.POST.get("content")))
        comment.save()
        return redirect("blog:post-detail")
