from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from ecommerce import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import jwt,uuid



# class RegisterSerializer(serializers.ModelSerializer):
#     is_active=serializers.BooleanField(default=True)
    
#     class Meta:
#         model=CustomUser
#         fields=['is_active','email','password']
        
    
class RegisterSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = CustomUser
        fields = ['is_active', 'email', 'password']

    def create(self, validated_data):

        email = validated_data.get('email')

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = True
        token_payload = {
            'email': email,
            'secret_token': str(uuid.uuid4())
        }
        token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')

        # Create user
        user = CustomUser.objects.create(**validated_data)

        # Generate activation link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = f"http://127.0.0.1:8000/account/activate/{uid}/{token}/"


        # Send activation email
        html_content = render_to_string('index.html', {'email': user.email, 'activation_link': activation_link})
        subject = 'Activate Your Account'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(subject, '', from_email, recipient_list, html_message=html_content)
        except Exception as e:
            raise serializers.ValidationError({'error': f"Failed to send email: {str(e)}"})

        return user

        

   

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','password']
        
class GetSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['name','phone','address','image','role']

class DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'
        

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['password']

class ForgetPasswordSeriaalizer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['password']
    
    # def create(self, validated_data):
    #     return super().create(validated_data)
        
    
        