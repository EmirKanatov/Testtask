from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.generics import get_object_or_404

from .models import Profile


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    nickname = serializers.CharField(max_length=128)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if User.objects.filter(username=attrs['username']).count() > 0:
            raise serializers.ValidationError({"username": "Username is already taken"})
        if Profile.objects.filter(nickname=attrs['nickname']).count() > 0:
            raise serializers.ValidationError({"nickname": "Nickname is already taken"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        profile = Profile.objects.get(user=user)
        profile.nickname = validated_data['nickname']
        profile.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        if not user:
            raise serializers.ValidationError('Access denied: wrong username or password.', code='authorization')
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("Wrong password", code='authorization')

        attrs['user'] = user
        return attrs


class RestorePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=8)
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError('Wrong password')
        return password

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return super().validate(attrs)

    def set_new_password(self):
        user = self.context['request'].user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'nickname'
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(source="userprofile", many=False)

    class Meta:
        model = User
        fields = ['profile', 'username']

    def update(self, instance, validated_data):
        userprofile_serializer = self.fields['profile']
        userprofile_instance = instance.userprofile
        userprofile_data = validated_data.pop('userprofile', {})

        userprofile_serializer.update(userprofile_instance, userprofile_data)
        instance = super().update(instance, validated_data)

        instance.save()
        return instance


