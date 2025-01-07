from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from .serializer import DutyModelSerializer
from ...models import Duty
from .permissions import IsOwner
from .paginations import DutyPagination

"""model viewset for implement CRUD for duties"""
class DutyModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = DutyModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {'done_status':['exact'],'deadline_date':['gt','lt']}
    search_fields = ['title', 'description']
    ordering_fields = ['done_status','deadline_date']
    pagination_class = DutyPagination
    
    
    """ override get_queryset method in order to each user could see only his/her own duties"""
    def get_queryset(self):
        return Duty.objects.filter(author__user__id=self.request.user.id)