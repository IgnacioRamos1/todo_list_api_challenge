from rest_framework import generics
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import response, status
from django.contrib.auth import authenticate


class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

register_user_view = RegisterAPIView.as_view()


class LoginAPIView(generics.GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)

        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data, status=status.HTTP_200_OK)
        
        return response.Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

login_user_view = LoginAPIView.as_view()
