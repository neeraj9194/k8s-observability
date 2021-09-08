from django.contrib.auth.models import User
from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Article

TRIMMED_SUMMARY_LETTERS = 100


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='author'
    )

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'read_time', 'published',
                  'updated_ts', 'created_ts', 'content', 'author_id']


class ArticleSummarySerializer(serializers.ModelSerializer):
    author = UserSerializer()
    content_summary = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'author', 'title', 'read_time', 'published',
                  'updated_ts', 'created_ts', 'content_summary']

    def get_content_summary(self, article):
        return article.content[:TRIMMED_SUMMARY_LETTERS]
