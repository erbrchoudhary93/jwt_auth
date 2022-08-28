from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializers, UserPasswordResetSerializer, UserRegistractionSerializers,UserProfileSerializer,UserChangePasswordSerializer,Sendpasswordresetserializer
from account.renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.


# Token generate manully
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistractionView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,formet=None):
        serializer = UserRegistractionSerializers(data =request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            
            return Response({'token':token,"msg":"Registraction Successful"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
# class AccountVerifyView(APIView):
#     renderer_classes = [UserRenderer]
#     def get(self,request,formet=None):
#         serializer =UserProfileSerializer(request.user)
#         # if serializer.is_valid():
#         return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
    
class UserLoginView(APIView):
    def post(self,request,formet=None):
        serializer = UserLoginSerializers(data =request.data)
        if serializer.is_valid():
            email =serializer.data.get('email')
            password =serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":"Login Succes"},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}},status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,formet=None):
        serializer =UserProfileSerializer(request.user)
        # if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self,request,formet=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
class SendPasswodResetEmailView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,formet=None):
        serializer = Sendpasswordresetserializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link send Successfully  please check your email  !!'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
        
    
class UserPasswordResetView(APIView):
    renderer_classes =[UserRenderer]
    def post(self,request,uid,token,formet=None):
        serializer = UserPasswordResetSerializer(data =request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password  Reset Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    