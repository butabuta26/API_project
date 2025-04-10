from rest_framework import mixins, viewsets, response
# from .models import User
from .serializers import UserSerializer, RegisterSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from .models import EmailVerificationCode
import random

User = get_user_model()

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_code(user)
            return response.Response(
                {'detail': 'User registered successfully and verification code sent to email'},
                status=status.HTTP_201_CREATED
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def send_verification_code(self, user):
        code = str(random.randint(100000, 999999))
        
        EmailVerificationCode.objects.update_or_create(
            user=user,
            defaults={'code':code, 'created_at': timezone.now()}
        )
        subject = 'Your verification code'
        message = f'Hello {user.username}, your verification code is {code}'
        send_mail(subject, message, 'no-reply@example.com', [user.email])
           
class ResetPasswordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            # reset_url = f'http://127.0.0.1:8000/reset_password_confirm/{uid}/{token}/'
            
            send_mail(
                'პაროლის აღდგენა',
                f'დააჭირე ბმულს, რომ აღადგინო პაროლი: {reset_url}',
                'noreply@example.com',
                [user.email],
                fail_silently=False
            )
            
            return Response({'message: წერილი წარმატებით არის გაგზავნილი'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordConfirmViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description='User ID (Base64 encoded)', type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description='Password Reset Token', type=openapi.TYPE_STRING)
            ]
    )
    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)