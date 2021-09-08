from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from prometheus_client import Counter

from .serializers import UserSerializer

c = Counter('user_list_call',
            'Number get(list) request user api received')


class UserApi(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        c.inc()
        return super(UserApi, self).list(self, request, *args, **kwargs)
