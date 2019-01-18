from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import Sitting


class UserSerializer(serializers.ModelSerializer):
    """
    Handles the retrieval of a user
    """
    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):
    """
    Handles the creation of a user and the retrieval of the JWT token
    And also the validation of a user
    """

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        """
        Retrieves a JWT token to authenticate a user
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        """
        Creates a user in the database
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'first_name', 'password')
        extra_kwargs = {'first_name': {'required': True}}


class SittingSerializer(serializers.ModelSerializer):
    """
    Handles the validation and JSON of a sitting object.
    """

    class Meta:
        model = Sitting
        fields = ('user', 'quiz', 'user_choices', 'score')
