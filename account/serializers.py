from django.utils.encoding import smart_str ,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers
from account.models import Customuser
from  .utils import Utils


class UserRegistractionSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":'password'},write_only=True)
    class Meta:
        model = Customuser
        fields =['email','name','password','password2','tc']
        extra_kwargs = {
            'password':{'write_only':True}
            }
        
        
    #Validating password and conform password while Registraction
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and conform password dosen't match")
        return attrs
    
    
    def create(self, validated_data):
        return Customuser.objects.create_user(**validated_data)
    
    
class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model=Customuser
        fields = ['email','password']
        
        
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id','email','name']
        
        
class UserChangePasswordSerializer(serializers.Serializer):
    password= serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields =['passwod','password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and conform password dosen't match")
        
        user.set_password(password)
        user.save()
        return attrs
        

class Sendpasswordresetserializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields =['email']
    
    
    def validate(self, attrs):
        email = attrs.get('email')
        if Customuser.objects.filter(email = email):
            user = Customuser.objects.get(email=email)
            uid =urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded Uid : ",uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("password Reset token ",token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print("password Reset link  : ",link)
            body = "Click following link to reset password \n \n " + link
            # send email
            data={
                'subject' :"Reset your Password"  ,
                'body':body,
                'to_email':user.email  ,
            }
            Utils.send_email(data)
            return attrs 
            
        else:
            raise serializers.ValidationError("You are not Registered user")
        
        
class UserPasswordResetSerializer(serializers.Serializer):
    password= serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    password2= serializers.CharField(max_length = 255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields =['passwod','password2']
        
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and conform password dosen't match")
            
            id = smart_str(urlsafe_base64_decode(uid))
            print(id)
            user = Customuser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not valid or expaired")
            user.set_password(password)
            user.save()
            return attrs
            
        except DjangoUnicodeDecodeError as identifier:
            print(identifier)
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or expaired")
            