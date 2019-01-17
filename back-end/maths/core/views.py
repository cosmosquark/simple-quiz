from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, \
SittingSerializer
from .models import Sitting
from quiz.models import Quiz

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Handle Access to the User Database
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        """
        Add a new user to our User Table
        """
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SittingAPI(APIView):
    """
    Handle Access to the Quiz sitting
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None):
        """
        Get the quiz sitting for the current user. If it does not exist, then create it.
        """
        if pk is None:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        sit, created = Sitting.objects.get_or_create(user=request.user, quiz_id=pk)
        serializer = SittingSerializer(sit)
        return Response(serializer.data)

    def post(self, request, pk=None):
        """
        Post answers in response to a quiz, where pk is the quiz id which the user is answering
        """
        if pk is None:
            return Response({'response': 'Invalid Quiz ID'}, status=status.HTTP_400_BAD_REQUEST)

        if "user_choices" not in request.data:
                return Response({'response': 'Missing User Choices'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "user_choices": request.data["user_choices"],
            "quiz": pk
        }

        try:
            sitting = Sitting.objects.get(user=request.user, quiz=data["quiz"])
        except ObjectDoesNotExist:
            return Response({'response': 'Invalid Quiz or User'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = SittingSerializer(sitting, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"success": True, "response": serializer.data})
