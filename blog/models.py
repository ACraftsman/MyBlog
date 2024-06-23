from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)
    # 文章正文
    body = models.TextField('正文')
    # 文章创建时间和文章最后一次修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    # 文章摘要 默认情况下 CharField 要求我们必须存入数据，否则就会报错.
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此  # 使用 models.CASCADE 参数，意为级联删除。
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,  verbose_name='标签', blank=True)
    # User 是从 django.contrib.auth.models导入的.
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body)[:54])
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
