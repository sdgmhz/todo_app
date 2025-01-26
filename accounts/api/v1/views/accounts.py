from rest_framework import generics
from ..serializers import (RegistrationSerializer,
                        CustomAuthTokenSerializer,
                        CustomTokenObtainPairSerializer,
                        ChangePasswordSerializer,
                        ActivationResendAndPasswordResetSerializer,
                        PasswordResetConfirmSerializer,
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
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from jwt import decode
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.conf import settings


User = get_user_model()


''' registration view '''
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'email': serializer.validated_data['email']}
            user_obj = get_object_or_404(User, email=data['email'])
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token, 'email':data['email'], 'request':request}, 'admin@admin.com', to=[data['email']])
            EmailThread(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # this method creates access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
    

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
    
        
    
# user activation view
class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):
        try:
            # decode token and find the user_id
            token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        # find user and verify it
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"detail": "your account has already been verified"})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"detail": "Your account has been verified and activated successfully"}, status=status.HTTP_200_OK)


# resend activation link view    
class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendAndPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        if not user_obj.is_verified:
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl',
                                      {'token':token, 'email': email},
                                        'admin@admin.com',
                                        to=[email],
                                        )

            EmailThread(email_obj).start()
            return Response({"detail": "user activation email resend successfully"}, status=status.HTTP_200_OK)
        return Response({"detail": "your account has already been verified"})
    
        # this method creates access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
        

# send password reset link view
class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = ActivationResendAndPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
           # according to security considerations, we will not tell the user if there is no account associated with this email or not!!
            return Response({"detail": "If there is an account with this email, we will send an password reset link for you. Check your inbox!"}, status=status.HTTP_200_OK)
        if user_obj.is_verified:
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage('email/password_reset_email.tpl',
                                        {'token':token, 'email': email},
                                        'admin@admin.com',
                                        to=[email],
                                        )

            EmailThread(email_obj).start()
           # according to security considerations, we will not tell the user if there is no account associated with this email or not!!
            return Response({"detail": "If there is an account with this email, we will send an password reset link for you. Check your inbox!"}, status=status.HTTP_200_OK)
        return Response({"detail": "Your account is not verified. First you should request for user verification. "}, status=status.HTTP_400_BAD_REQUEST)
    
        # this method creates access token for user
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
    

class PasswordResetConfirmApiView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    
    def get(self, request, token, *args, **kwargs):
        try:
            # decode token and find the user_id
            token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        # find user
        user_obj = User.objects.get(pk=user_id)
        return Response({"detail": f"Password reset for user: {user_obj.email}"}, status=status.HTTP_200_OK)
                        
    
    def put(self, request, token, *args, **kwargs):
        try:
            # decode token and find the user_id
            token = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({"detail": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        # find user for resetting password
        user_obj = User.objects.get(pk=user_id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
           
            # set the new password
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            return Response({"detail": f"password reset successfully for user:{user_obj.email}"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
        

        
        


 