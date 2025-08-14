from rest_framework import generics, status
from django.shortcuts import render
from rest_framework import generics
from .serializers import SignupSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from transactions.models import Wallet

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create JWT token pair
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access_token)
        }, status=status.HTTP_201_CREATED)

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_id = response.data.get("id")
        if user_id:
            Wallet.objects.create(user_id=user_id)  # Create wallet for new user
        return response