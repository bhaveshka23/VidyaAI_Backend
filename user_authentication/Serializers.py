from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

class SignupSerializer(serializers.ModelSerializer):
    lang = serializers.CharField()
    education = serializers.CharField()
    age = serializers.IntegerField()
    grade = serializers.CharField()
    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name",
                  "lang", "education", "age", "grade"]

    def create(self,validated_data):

        lang = validated_data.pop("lang")
        education = validated_data.pop("education")
        age = validated_data.pop("age")
        grade = validated_data.pop("grade")

        #create the user

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )

        Profile.objects.create(
            user=user,
            lang=lang,
            education=education,
            age=age,
            grade=grade
        )
        return user

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "school_id": user.username,
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
