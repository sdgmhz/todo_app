from rest_framework import generics
from ..serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from ....models import Profile
from django.shortcuts import get_object_or_404

# profile view
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes =[IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj