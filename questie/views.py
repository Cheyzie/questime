from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,Http404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, DudeSerializer, QuizDetailSerializer

from .models import Quiz,Question,Choice,Dude

# Create your views here.

class QuizzesView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.filter(is_public=True).order_by('creation_date')
        serializer = QuizSerializer(quizzes,many=True)
        return Response({"quizzes":serializer.data})
    def post(self,request):
        received_quiz = request.data.get('quiz')
        quiz_serializer = QuizDetailSerializer(data=received_quiz)
        if quiz_serializer.is_valid():
            quiz_obj = quiz_serializer.save()
            return Response({'action':'create quiz success','quiz_id':quiz_obj.id,})
        return Response(status=404,data={'error_message':quiz_serializer.errors})

class QuizView(APIView):
    def get(self,request,pk):
        quiz = Quiz.objects.get(pk=pk)
        quiz_serializer = QuizDetailSerializer(quiz,many=False)
        quiz_data = quiz_serializer.data
        questions_data = []
        for question in quiz_data.pop('questions'):
            choices = question.pop('choices')
            questions_data.append({'question': question, 'choices': choices})
        return Response({'quiz':quiz_data,'questions': questions_data})

class AnswerView(APIView):
    def get(self, request, pk):
        dudes = Dude.objects.filter(quiz_id=pk)
        serializer = DudeSerializer(dudes,many=True)
        return Response({'dudes':serializer.data})

    def post(self, request, pk):
        try:
            dude_name = request.data.get('name')
            answers = request.data.get('answers')
            if not dude_name or not answers:
               return Response(status=404) 
        except:
            return Response(status=404)

        quiz_id = pk
        quiz = Quiz.objects.get(pk=pk)
        correct_answers = 0

        for answer in answers:
            question_id = answer["question_id"]
            choices_id = answer["choices_id"]
            correct_answers += Question.objects.get(pk=question_id).check_answers(choices_id)
        rating = correct_answers/len(Quiz.objects.get(pk=quiz_id).questions.all())
        serializer = DudeSerializer(data={'name':dude_name, 'quiz_id':quiz_id, 'rating':rating})
        serializer.is_valid()
        serializer.save()
        return Response({'name':dude_name, 'rating':rating, 'quiz_id': quiz_id, 'quiz_name': quiz.quiz_name})
