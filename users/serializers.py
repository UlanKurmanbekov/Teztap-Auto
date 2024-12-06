from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'phone_number', 'email']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'patronymic', 'last_name',  'phone_number','password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'patronymic': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            patronymic=validated_data['patronymic'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()
