from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Article(models.Model):
    """
    Article model for blog post.
    """
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    read_time = models.IntegerField(default=0)
    published = models.BooleanField(default=False)
    content = models.TextField()
    updated_ts = models.DateTimeField(auto_now=True)
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_ts"]

    def __str__(self) -> str:
        return self.title
