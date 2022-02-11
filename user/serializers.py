from rest_framework import serializers
from . models import VirtualWalletUser
from transactions.models import Wallet

from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = VirtualWalletUser
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('id', 'first_name', 'last_name', 'password', 'email', 'birth_date')

    def create(self, validated_data):
        user = VirtualWalletUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Wallet.objects.create(owner=user)
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    class Meta:
        model = VirtualWalletUser
        fields = ['email', 'password']

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

