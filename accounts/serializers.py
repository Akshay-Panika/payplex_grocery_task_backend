from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'terms_accepted']

    def validate(self, attrs):
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError({
                "terms_accepted": "Please accept terms and conditions."
            })
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            terms_accepted=validated_data['terms_accepted']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs