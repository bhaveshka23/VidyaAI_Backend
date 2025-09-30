from django.core.mail import send_mail
from google.protobuf.proto import serialize
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .Serializers import SignupSerializer,LoginSerializer , ProfileSerializer
import random
from django.shortcuts import get_object_or_404
from .models import Profile


# Function to send email
def send_school_id_notification(email, school_id):
    subject = "Your School ID for VidyaAI"
    message = f"Welcome to VidyaAI! Your School ID is: {school_id}"
    sender = "vidyaai884@gmail.com"
    print('email sended successfully')
    send_mail(subject, message, sender, [email], fail_silently=True)

# Function to generate school id
def generate_school_id():
    return f"vidya{random.randint(1000, 9999)}"

class SignUp(APIView):
    def post(self, request):
        data = request.data.copy()

        # Generate School ID
        school_id = generate_school_id()
        data["username"] = school_id   # use it as username

        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Send email notification
            send_school_id_notification(data.get("email"), school_id)

            return Response(
                {"message":"User Created Successfully",
                 "school_id":school_id,
                 "user_id" :user.id},
                 status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProFile(APIView):
    def get(self, request, id):
        try:
            profile = get_object_or_404(Profile, id=id)
            serializer = ProfileSerializer(profile)

            return Response(
                {
                    "success": True,
                    "user": serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )






