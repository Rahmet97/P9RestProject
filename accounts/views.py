from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


class RegisterAPIView(APIView):

    def post(self, request):
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        email = request.data.get('email')
        username = request.data.get('username')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'error': 'This username already exists!'}, status=405)
            if User.objects.filter(email=email).exists():
                return Response({'error': 'This email already exists!'}, status=405)
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = User.objects.get(username=username)
            user.set_password(password1)
            user.save()
        else:
            return Response({'error': 'Passwords are not same!'}, status=405)
        return Response(status=201)
