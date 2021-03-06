from core.serializers import UserSerializer


def my_jwt_response_handler(token, user=None, request=None):
    """
    Function to add a new user field with the user's serialized data when
    a token is generated. This is our default JWT response handler
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }
