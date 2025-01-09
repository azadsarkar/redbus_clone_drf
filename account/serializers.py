from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import password_validation


class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField( write_only = True, required = False)
    class Meta :
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password','password2']
        extra_kwargs = {'password': {'write_only': True}, }


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username',instance.username)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)

        instance.password = make_password(validated_data.get('password',instance.password))
        instance.save()
        return instance
        
   

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
    

class UserUpdateDeleteserializer(serializers.ModelSerializer):
    class Meta :
        model = User
        fields = ['username', 'first_name', 'last_name','email']

    
    # def update(self, instance, validated_data):
    #     breakpoint()
    #     return super().update(instance, validated_data)


class UserChangePassword(serializers.Serializer):

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        # breakpoint()
        if not user.check_password(value):
            raise serializers.ValidationError(
                ('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': ("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user
    