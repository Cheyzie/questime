from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, DudeSerializer, QuizDetailSerializer,\
    ImageSerializer, ResultSerializer, DudeDetailSerializer
import uuid, traceback
from .models import Quiz, Question, Choice, Dude, Image

# Create your views here.

class QuizzesView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.filter(is_public=True).order_by('creation_date')
        serializer = QuizSerializer(quizzes,many=True)
        return Response({"quizzes":serializer.data})

    def post(self, request):
        try:
            received_quiz = request.data.get('quiz')
        except:
            return Response(data={'message': 'invalid data'},status=status.HTTP_400_BAD_REQUEST)
        else:
            quiz_serializer = QuizDetailSerializer(data=received_quiz)
            if quiz_serializer.is_valid():
                quiz_obj = quiz_serializer.save()
                return Response({'action':'create quiz success','quiz_id':quiz_obj.id,})
            return Response(data={'error_message':quiz_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class QuizView(APIView):

    def get(self,request,pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({'message':'invalid quiz id'}, status=status.HTTP_404_NOT_FOUND)
        quiz_serializer = QuizDetailSerializer(quiz,many=False)
        quiz_data = quiz_serializer.data
        questions_data = []
        for question in quiz_data.pop('questions'):
            choices = question.pop('choices')
            questions_data.append({'question': question, 'choices': choices})
        return Response({'quiz':quiz_data,'questions': questions_data}, status=status.HTTP_200_OK)


class DudesView(APIView):

    def get(self, request):
        dudes = Dude.objects.all()
        serializer = DudeSerializer(dudes, many=True)
        return Response({'dudes': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        dude = request.data.get('dude')
        serializer = DudeSerializer(data=dude)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['editing_key'] = Dude.objects.get(pk = serializer.data['id']).editing_key
            return Response({'message': 'Hi ' + serializer.data['name'], "dude": data}, 
                status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DudeView(APIView):

    def get(self, request, pk):
        try:
            dude = Dude.objects.get(pk=pk)
        except Dude.DoesNotExist:
            return Response({'message': 'invalid dude id'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DudeDetailSerializer(dude)
        return Response({'dude': serializer.data})
    
    def delete(self, request, pk):
        try:
            editing_key = request.data.get('editing_key')
        except ValueError:
            return Response({'message': 'no edit_key'}, status=status.HTTP_403_FORBIDDEN)
        try:
            dude = Dude.objects.get(pk=pk)
        except:
            return Response({'message': 'invalid dude id'}, status=status.HTTP_404_NOT_FOUND)
        if editing_key == dude.editing_key:
            dude.delete()
            return Response({'message': 'deleting success'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'invalid edit_key'}, status=status.HTTP_403_FORBIDDEN)


class ResultsView(APIView):
    def get(self, request, pk):
        results = Quiz.objects.get(pk=pk).results.all()
        serializer = ResultSerializer(results,many=True)
        return Response({'results':serializer.data})

    def post(self, request, pk):
        try:
            dude_id = request.data.get('dude_id')
            answers = request.data.get('answers')
            if not dude_id or not answers:
               return Response(status=400)
        except:
            return Response(status=400)
        try:
                dude = Dude.objects.get(id=dude_id)
        except:
            return Response({'message': 'dude is not found'}, status=status.HTTP_403_FORBIDDEN)
        try:
            quiz = Quiz.objects.get(pk=pk)
        except:
            return Response({'message': 'quiz is not found'}, status=status.HTTP_404_NOT_FOUND)
        
        correct_answers = 0

        for answer in answers:
            question_id = answer["question_id"]
            choices_id = answer["choices_id"]
            correct_answers += Question.objects.get(pk=question_id).check_answers(choices_id)
        rating = correct_answers/len(Quiz.objects.get(pk=pk).questions.all())
        data={'dude':dude_id, 'quiz':pk, 'rating':rating}
        serializer = ResultSerializer(data=data)
        if serializer.is_valid():
            try:
                dude.results.get(quiz=quiz).delete()
            except:
                pass
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ImagesView(GenericAPIView):

    serializer_class = ImageSerializer

    def get(self, request):
        serializer = ImageSerializer(Image.objects.all(), many=True)
        return Response({'images': serializer.data})

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['editing_key'] = Image.objects.get(pk = serializer.data['id']).editing_key
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):
    def get(self, request, pk):
        try:
            image = Image.objects.get(pk=pk)
        except:
            return Response({'message':'invalid image id'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            editing_key = request.data.get('editing_key')
        except ValueError:
            return Response({'message': 'no edit_key'}, status=status.HTTP_403_FORBIDDEN)
        try:
            image = Image.objects.get(pk=pk)
        except:
            return Response({'message': 'invalid image id'}, status=status.HTTP_404_NOT_FOUND)
        if editing_key == image.editing_key:
            image.delete()
            return Response({'message': 'deleting success'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'invalid edit_key'}, status=status.HTTP_403_FORBIDDEN)


# {"dude_id":"cdddc21b-7f7e-4e15-87ef-9169a921b37d","answers":[{"question_id":"4133c3ff-98d7-4ba1-b5c4-77ae49603f0d","choices_id":["7fc62f29-1914-48df-855b-736b04db098c"]},{"question_id":"71351197-1add-4f99-9dab-b06de1c76deb","choices_id":["1417aa78-9f12-4fa1-8ee0-6557352da053"]}]}
# {"dude_id":"928cdff8-2542-45b5-bddc-c3574da82663","answers":[{"question_id":"c0a9fa29-1e0a-433d-9f54-090e8a98e765","choices_id":["1892bb83-41dd-424c-b4c2-dec920c0c0e9","8e305407-3dba-4794-93b8-3cfb9376957f"]},{"question_id":"391b2ca1-dcf3-4b45-81b4-84a9764cfb17","choices_id":["f2915eca-f49d-4aae-b348-e0380125d11b"]}]} 