from django.shortcuts import render, redirect

from rest_framework import generics, status, views, permissions
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
# Create your views here.

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+ str(token)
        email_body = 'Hi' + user.username+'User link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email' : user.email, 'email_subject': 'Please verify your email'}
        
        Util.send_email(data)
        return Response(user_data,status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter('token',in_= openapi.IN_QUERY, description='Description',type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameter=[token_param_config])
    def get(self):
        token = request.Get.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIVIew(generics.GenericAPIView):

    serializer_class= LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):

    serializer_class = ResetPasswordEmailRequestSerializer

    
    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        
        email = request.data.get['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(user.id)
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={' uidb64' : uidb64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hi, \n Use the link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email' : user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response({'success': "A link to reset your password has been sent"}, status=status.HTTP_200_OK)
        

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self,request,uidb64,token):

        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'The Token has expired, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': True, 'message': 'Credentials Valid', 'uidb64': uidb64, 'token': token},status=status.HTTP_200_OK)

            
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error':'The Token has expired, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)


    def post(self,request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)