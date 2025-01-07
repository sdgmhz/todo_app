from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializer import DutyModelSerializer
from ...models import Duty

"""model viewset for implement CRUD for duties"""
class DutyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DutyModelSerializer
    
    
    """ override get_queryset method in order to each user could see only his/her own duties"""
    def get_queryset(self):
        return Duty.objects.filter(author__user__id=self.request.user.id)