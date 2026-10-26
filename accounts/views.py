from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdministrator
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new student account.
    """

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Registration successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CurrentUserView(APIView):
    """
    Return information about the currently authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_authenticated": user.is_authenticated,
            }
        )


class AdministratorTestView(APIView):
    """
    Test that only administrators can access this endpoint.
    """

    permission_classes = [IsAdministrator]

    def get(self, request):
        return Response(
            {
                "message": "Administrator access confirmed.",
                "username": request.user.username,
                "role": request.user.role,
            }
        )
