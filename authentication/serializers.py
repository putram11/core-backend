from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer untuk registrasi user menggunakan model User bawaan Django"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate_email(self, value):
        """Validasi email harus unik"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email sudah digunakan.")
        return value
    
    def validate(self, attrs):
        """Validasi password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password tidak cocok."})
        return attrs
    
    def create(self, validated_data):
        """Membuat user baru"""
        validated_data.pop('password_confirm', None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer untuk login user"""
    
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Validasi kredensial login"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            # Coba login dengan username atau email
            user = authenticate(username=username, password=password)
            if not user:
                # Coba dengan email jika username gagal
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if not user:
                raise serializers.ValidationError("Username/email atau password salah.")
            
            if not user.is_active:
                raise serializers.ValidationError("Akun tidak aktif.")
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError("Username dan password harus diisi.")


class UserSerializer(serializers.ModelSerializer):
    """Serializer untuk data user bawaan Django"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer untuk mengubah password"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        """Validasi password lama"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password lama salah.")
        return value
    
    def validate(self, attrs):
        """Validasi password baru"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password baru tidak cocok."})
        return attrs
