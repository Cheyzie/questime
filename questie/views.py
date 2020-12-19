from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,Http404
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, DudeSerializer


from .models import Quiz,Question,Choice,Dude

# Create your views here.
def index(request):
    return HttpResponse("{'name':'Classtime','action':'Suck'}")

class QuizzesView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.filter(is_public=True).order_by('creation_date')
        serializer = QuizSerializer(quizzes,many=True)
        return Response({"quizzes":serializer.data})
    def post(self,request):
        received_quiz = request.data.get('quiz')
        received_questions = request.data.get('questions')
        quiz_serializer = QuizSerializer(data=received_quiz)
        if quiz_serializer.is_valid():
            quiz_obj = quiz_serializer.save()
            for received_question in received_questions:
                is_valid_question = {'question':'','choices': [], }
                question = received_question['question']
                question['quiz_id'] = quiz_obj.id
                question_serializer = QuestionSerializer(data=question)
                if question_serializer.is_valid():
                    question_obj = question_serializer.save()
                    for choice in received_question['choices']:
                        choice['question_id'] = question_obj.id
                        choice_serializer = ChoiceSerializer(data=choice)
                        if choice_serializer.is_valid():
                            choice_serializer.save()

            return Response({'action':'create quiz','received_quiz':received_quiz,'recived_questions':received_questions})
        return Response({'message':'Шо за Саня долбить хуйові реквксти?'})

class QuizView(APIView):
    def get(self,request,pk):
        quiz = get_object_or_404(Quiz,pk=pk)
        quiz_serializer = QuizSerializer(quiz,many=False)
        questions = quiz.question_set.all()
        quiz_response = {'quiz':quiz_serializer.data,'questions':[]}
        for question in questions:
            question_serializer = QuestionSerializer(question)
            choices = question.choice_set.all()
            choices_serializer = ChoiceSerializer(choices,many=True)
            quiz_response['questions'].append({'question': question_serializer.data,
            'choices':choices_serializer.data})
        return Response(quiz_response)

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
        correct_answers = 0

        for answer in answers:
            quiz_id = pk
            question_id = answer["question_id"]
            choices_id = answer["choices_id"]
            correct_answers += Question.objects.get(pk=question_id).check_answers(choices_id)
            # correct_choices = Question.objects.get(pk=question_id).choice_set.filter(is_correct=True)
            # if len(choices_id) > 0:
            #     if(Question.objects.get(pk=question_id).is_multiple_choice):
            #         for choice_id in choices_id:
            #             correct_answers+=len(correct_choices.filter(pk=choice_id))/len(correct_choices)
            #     else:
            #         if(len(correct_choices.filter(pk=choices_id[0]))>0):
            #             correct_answers+=1
        rating = correct_answers/len(Quiz.objects.get(pk=quiz_id).question_set.all())
        serializer = DudeSerializer(data={'name':dude_name, 'quiz_id':quiz_id, 'rating':rating})
        serializer.is_valid()
        serializer.save()
        return Response({'name':dude_name, 'rating':rating})


            



    
        
