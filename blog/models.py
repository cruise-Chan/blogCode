from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '分类'


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '标签'


class Post(models.Model):
    title = models.CharField(max_length=70, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改时间')
    # 文章摘要
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='文章摘要')
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    # User是django为我们写好的用户模型
    author = models.ForeignKey(User, verbose_name='作者',
                               on_delete=models.DO_NOTHING,)
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time', 'title']
        verbose_name_plural = '文章'

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            # strip_tags 去掉 HTML 文本的全部HTML标签
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)


