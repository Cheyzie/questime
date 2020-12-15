from .models import Quiz,Question,Choice,Dude
from rest_framework import serializers

class QuizSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    quiz_name = serializers.CharField(max_length=50)
    creation_date = serializers.DateTimeField(read_only=True)
class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    quiz_id = serializers.IntegerField()
    wording = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=250)
    image = serializers.CharField(max_length=100)
    is_multiple_choice = serializers.BooleanField()

class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_id = serializers.IntegerField()
    text = serializers.CharField(max_length=100)
    is_correct = serializers.BooleanField(write_only=True)


