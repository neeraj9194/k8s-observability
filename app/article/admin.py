from django.contrib import admin

from article.models import Article


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    """
    Article model admin pannel.
    """


admin.site.register(Article, ArticleAdmin)
