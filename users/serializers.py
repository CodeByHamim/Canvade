from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from .models import CustomUser

user = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name']
        
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])

    def validate_new_password(self, value):
        validate_password(value)
        return value
    
# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         if not user.objects.filter(email=value).exists():
#             raise serializers.ValidationError("No user found with this email.")
#         return value

#     def save(self):
#         user_instance = user.objects.get(email=self.validated_data['email'])
#         uid = urlsafe_base64_encode(force_bytes(user_instance.pk))
#         token = default_token_generator.make_token(user_instance)

#         # 🔧 Correctly appending query params
#         reset_url = self.context['request'].build_absolute_uri(
#         reverse('password-reset-confirm') + f"?uid={uid}&token={token}"
#         )

#         send_mail(
#             subject="Password Reset Request",
#             message=f"Hi {user_instance.username},\n\nClick the link below to reset your password:\n{reset_url}",
#             from_email="no-reply@canvade.com",
#             recipient_list=[user_instance.email],
#         )

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     uid = serializers.CharField()
#     token = serializers.CharField()
#     new_password = serializers.CharField(min_length=8)

#     def validate(self, attrs):
#         try:
#             uid = force_str(urlsafe_base64_decode(attrs['uid']))
#             user_instance = user.objects.get(pk=uid)
#         except (user.DoesNotExist, ValueError, TypeError, OverflowError):
#             raise serializers.ValidationError("Invalid user.")

#         if not default_token_generator.check_token(user_instance, attrs['token']):
#             raise serializers.ValidationError("Invalid or expired token.")

#         attrs['user'] = user_instance
#         return attrs

#     def save(self):
#         user = self.validated_data['user']
#         user.set_password(self.validated_data['new_password'])
#         user.save()

class logoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail("bad_token")