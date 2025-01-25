from rest_framework import generics
from ..serializers import (RegistrationSerializer,
                        CustomAuthTokenSerializer,
                        CustomTokenObtainPairSerializer,
                        ChangePasswordSerializer,
                        ) 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from mail_templated import EmailMessage
from ...utils import EmailThread


''' registration view '''
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'email': serializer.validated_data['email']}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

''' customizing obtain auth token view in order to return more details '''
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                })
    

# token discard view
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# customizing jwt creating view in order to override serializer
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# change password view
class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.serializer_class(data=request.data, context={'user':request.user})
        if serializer.is_valid():
            # check if the old password is entered correctly
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"detail": "old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            # set the new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TestEmailSend(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        email_obj = EmailMessage('email/hello.tpl', {'name': 'ali'}, 'admin@admin.com',
                       to=['sdg.mhz@gmail.com'])
        EmailThread(email_obj).start()
        
        return Response("email sent")
    


        