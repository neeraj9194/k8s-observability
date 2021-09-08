from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from prometheus_client import Counter
from .models import Article
from .serializers import ArticleSummarySerializer, ArticleSerializer


class ArticlePagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


c = Counter('article_list_call',
            'Number get(list) request article api received')


class ArticleApi(ModelViewSet):
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSummarySerializer
        return ArticleSerializer

    def list(self, request, *args, **kwargs):
        c.inc()
        return super(ArticleApi, self).list(self, request, *args, **kwargs)
