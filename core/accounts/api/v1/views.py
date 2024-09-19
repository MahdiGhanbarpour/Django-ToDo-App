from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from ...models import PasswordReset

User = get_user_model()

class RegistrationApiView(generics.GenericAPIView):
    '''
    A class to register the user and then send the activation token to his email
    '''
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            
            data = {
                "username":username,
                "email":email,
            }
            
            user_object = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_object)

            email_object = EmailMessage('email/activation_email.tpl', {'token': token}, "mahdi.ghanbarpour1387@gmail.com",to=[email])
            EmailThread(email_object).start()
            
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)

class CustomAuthToken(ObtainAuthToken):
    '''
    A class to create or receive user token
    '''
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
        
class CustomDiscardAuthToken(APIView):
    '''
    A class to log out and destroy the user token
    '''
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    '''
    A class to get tokens based on simple_jwt
    '''
    serializer_class = CustomTokenObtainPairSerializer
    
class ChangePasswordApiView(generics.GenericAPIView):
    '''
    A class to change the password
    '''
    permission_classes = [IsAuthenticated]
    model = User
    serializer_class = ChangePasswordSerializer
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password":["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            
            return Response({"detail":"Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivationApiView(APIView):
    '''
    A class to activate the user account based on the sent token
    '''
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except jwt.ExpiredSignatureError:
            return Response({"detail":"Token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({"detail":"Token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_object = User.objects.get(pk=user_id)
        
        if user_object.is_verified:
            return Response({"detail":"Your account has already been verified"})
        
        user_object.is_verified = True
        user_object.save()
        
        return Response({"detail":"Your account has been verified and activated successfully"})
    
class ActivationResendApiView(generics.GenericAPIView):
    '''
    A class to resend the activation token to the user's email
    '''
    serializer_class = ActivationResendSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_object = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_object)

        email_object = EmailMessage('email/activation_email.tpl', {'token': token}, "mahdi.ghanbarpour1387@gmail.com",to=[user_object.email])
        EmailThread(email_object).start()
        
        return Response({"detail":"User activation resend successfully"}, status=status.HTTP_200_OK)
        
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return str(refresh.access_token)
    
class RequestPasswordResetApiView(generics.GenericAPIView):
    '''
    A class to create and send a password reset token to the user's email
    '''
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        
        user = get_object_or_404(User, username=username)

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            
            PasswordReset(username=username, token=token).save()

            email_object = EmailMessage('email/reset_password.tpl', {'token': token}, "mahdi.ghanbarpour1387@gmail.com",to=[email])
            EmailThread(email_object).start()

            return Response({'detail': 'Password reset email sent'}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ResetPasswordApiView(generics.GenericAPIView):
    '''
    Reset the password based on the entered token
    '''
    serializer_class = ResetPasswordSerializer

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['new_password']
        
        try:
            reset_obj = PasswordReset.objects.get(token=token)
        except PasswordReset.DoesNotExist:
            return Response({'detail':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        if reset_obj.is_expired():
            reset_obj.delete()
            return Response({'detail':'Token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=reset_obj.username)
        
        user.set_password(new_password)
        user.save()
        
        reset_obj.delete()
        
        return Response({'detail':'Password updated'}, status=status.HTTP_200_OK)