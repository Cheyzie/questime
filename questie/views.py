from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer


from .models import Quiz,Question,Choice,Dude

# Create your views here.
def index(request):
    return HttpResponse("{'name':'Classtime','action':'Suck'}")

class QuizView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.order_by('creation_date')
        serializer = QuizSerializer(quizzes,many=True)
        return Response({"quizzes":serializer.data})

class QuizDetailView(APIView):
    def get(self,request,pk):
        quiz = get_object_or_404(Quiz,pk=pk)
        quiz_serializer = QuizSerializer(quiz,many=False)
        questions = quiz.question_set.all()
        quiz_response = {'quiz':quiz_serializer.data,'questions':[]}
        for question in questions:
            question_serializer = QuestionSerializer(question)
            choices = question.choice_set.all()
            choices_serializer = ChoiceSerializer(choices,many=True)
            quiz_response['questions'].append(
                {'question': question_serializer.data,'choices':choices_serializer.data})
        return Response(quiz_response)
        