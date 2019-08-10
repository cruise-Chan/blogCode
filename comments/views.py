from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # commit=False 的作用是仅仅利用表单的数据生成Commit模型类的实例，但还不保存评论数据到数据库
            # 将评论和倍评论的文章关联起来
            comment.post = post
            comment.save()

            # 重定向 post 的详情页，实际上当redirect函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
            # 然后重定向到 get_absolute_url方法返回的 URL
            return redirect(post)
        else:
            comment_list = post.comment_set.all() # 相当于Comment.objects.filter(post=post)
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)

    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)