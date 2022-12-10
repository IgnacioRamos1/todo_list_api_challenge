from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework import response, status


class RegisterAPIView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

register_user_view = RegisterAPIView.as_view()
