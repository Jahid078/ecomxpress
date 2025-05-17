from django.shortcuts import render,redirect
from .models import CustomUser
from .serializer import RegisterSerializer,LoginSerializer,GetSerializer,UpdateSerializer,DeleteSerializer,ChangePasswordSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from django.utils.http import urlsafe_base64_decode
import jwt,uuid
from rest_framework import viewsets  
from ecommerce import settings
from core.permission import IsAuthanticationCustomUser
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone


class register_viewset(ModelViewSet):
    http_method_names=['post']
    serializer_class=RegisterSerializer
    queryset=CustomUser.objects.all()
    
    
    def get_serializer_context(self):
        email=self.request.data.get('email')
        password=self.request.data.get('password')
        return ({'email':email,'password':password})



class ActivateAccountViewSet(viewsets.ViewSet):
    http_method_names = ['get']

    def retrieve(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(pk=uid)

            if user.is_verified:  
               return redirect('account-already-activated')

            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            
            if decoded_token['email'] == user.email:
                user.is_verified = True  #
                user.save()
                return redirect('activation-success') 
            
            else:
                
                return redirect('activation-failed') 

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, CustomUser.DoesNotExist):
            return redirect('activation-failed')
    

def account_already_activated_view(request):
    return render(request,'account_already_activated.html')

def activate_success_view(request):
    return render(request, 'activation_success.html')

def activate_failed_view(request):
    return render(request,'activation_failed.html')


class login_viewset(ModelViewSet):
    http_method_names=['post']
    serializer_class=LoginSerializer
    queryset=CustomUser.objects.all()
    
    
    def create(self, request, *args, **kwargs):
        email=self.request.data.get('email')
        password=self.request.data.get('password')
        SECRET_KEY=settings.SECRET_KEY
        if not email or not password:

            
            return Response({'error':'Email or Password are requred'},status=status.HTTP_400_BAD_REQUEST)
        
        user=CustomUser.objects.filter(email=email).first()
        if  user:
            user_id=user.id
            
        else:
            return Response({'error':'user not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if not check_password(password, user.password):
        # if password !=user.password:
            return Response({'error': 'Password does not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        encoded_jwt = jwt.encode({'id':user_id, 'secret_token':str(uuid.uuid4())}, SECRET_KEY, algorithm='HS256')
        
        return Response({
            'token':encoded_jwt
        })
            

class get_viewset(ModelViewSet):
    http_method_names=['get']
    serializer_class=GetSerializer
    queryset=CustomUser.objects.all()
    permission_classes=[IsAuthanticationCustomUser]
    
    def get_queryset(self):
        id=self.request.user_id
        return CustomUser.objects.filter(id=id)
    
        
class update_viewset(ModelViewSet):
    http_method_names=['patch']
    serializer_class=UpdateSerializer
    permission_classes=[IsAuthanticationCustomUser]
    queryset=CustomUser.objects.all()
    
    
    def partial_update(self, request, *args, **kwargs):
        id=self.request.user_id
        requested_id=kwargs.get('pk')
        if int(requested_id)!=id:
            return Response({'error':'update only own profile ..'})
        
        user=CustomUser.objects.filter(id=id).first()
        if not user:
            return Response({'error':'user not found '})
        
        serializer=self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'successfully':'User updated successfully','updated_data': serializer.data}) 
        return Response(serializer.errors)

class delete_viewset(ModelViewSet):
    http_method_names=['delete']
    serializer_class=DeleteSerializer
    permission_classes=[IsAuthanticationCustomUser]
    queryset=CustomUser.objects.all()
    
    
    def get_queryset(self):
        id=self.request.user_id
        return CustomUser.objects.filter(id=id)


class change_password_viewset(ModelViewSet):
    http_method_names=['patch']
    permission_classes=[IsAuthanticationCustomUser]
    serializer_class=ChangePasswordSerializer
    queryset=CustomUser.objects.all()
    
    
    def partial_update(self, request, *args, **kwargs):
        id=self.request.user_id
        current_password=self.request.data.get('current_password')
        new_password=self.request.data.get('new_password')
        request_id=kwargs.get('pk')
        if int(request_id)!=id:
            return Response({'error':'only own update profile .'})
        
        user=CustomUser.objects.filter(id=id).first()
        if not user:
            return Response({'error':'user not found'})
        if not current_password or not new_password:
            return Response({'error':'new_password and current_password both are requred'})
        
        password=user.password
        if check_password(current_password,user.password):
            user.password=make_password(new_password)
            user.save()
            return Response({'password Update successfully'})
        else:
            return Response({'error':'Current password is incorrect'})
        

class forget_password_viewset(ModelViewSet):
    http_method_names=['post']
    serializer_class=ChangePasswordSerializer
    permission_classes=[IsAuthanticationCustomUser]
    queryset=CustomUser.objects.all()
    

    def create(self, request, *args, **kwargs):
        # user_id= request.user_id
        SECRET_KEY=settings.SECRET_KEY
        email=self.request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email).first()
        id=user.id
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        otp = random.randint(100000, 999999)
        has_otp=make_password(str(otp))
        encoded_jwt = jwt.encode({'id':id,'has_otp':has_otp ,'secret_token':str(uuid.uuid4())}, SECRET_KEY, algorithm='HS256')
        

        subject = 'Your OTP for Password Reset'
        html_message = f"""
        <html>
        <body>
            <h2>Password Reset OTP</h2>
            <p>Your One-Time Password (OTP) is:</p>
            <h1 style="color: #007bff;">{otp}</h1>
            <p> Do not share it with anyone.</p>
        </body>
        </html>
        """

        try:
            send_mail(subject, '', settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
        except Exception as e:
            return Response({'error': f'Failed to send OTP email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
    'message': 'OTP has been sent to your email',
    'token': encoded_jwt
}, status=status.HTTP_200_OK)


class otp_varification_viewset(ModelViewSet):
    http_method_names = ['post']
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthanticationCustomUser]
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        token = request.data.get('token')

        if not otp or not new_password or not token:
            return Response(
                {"detail": "OTP, new_password, and token are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decoded_data.get('id')
            hashed_otp = decoded_data.get('has_otp')

            if not user_id or not hashed_otp:
                raise jwt.InvalidTokenError()
            user=CustomUser.objects.filter(id=user_id).first()

            if not check_password(str(otp), hashed_otp):
                return Response(
                    {"detail": "Invalid OTP."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if new_password:
                hash_password=make_password(new_password)
                user.password = hash_password
                user.save()

            return Response(
                {"detail": "Password changed successfully."},
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        
        

