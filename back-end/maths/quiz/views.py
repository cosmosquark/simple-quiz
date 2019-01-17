from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quiz, Question
from .serializers import QuestionSerializer

# Create your views here.
class QuizAPI(APIView):
    """
    Handle Access to the Quiz sitting
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None):
        """
        Get the quiz sitting for the current user. If it does not exist, then create it.
        """
        if pk is None:
            return Response({'response': 'Invalid Quiz ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz = Quiz.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'response': 'Invalid Quiz ID'},
                            status=status.HTTP_404_NOT_FOUND)

        questions = Question.objects.filter(quiz__id = quiz.pk)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
