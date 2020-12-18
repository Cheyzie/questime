from .models import Quiz,Question,Choice,Dude
from rest_framework import serializers

class QuizSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    quiz_name = serializers.CharField(max_length=50)
    creation_date = serializers.DateTimeField(read_only=True)
    is_public = serializers.BooleanField(write_only=True)
    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

class QuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    quiz_id = serializers.UUIDField()
    wording = serializers.CharField(max_length=100)
    text = serializers.CharField(max_length=2500,required=False)
    image = serializers.CharField(max_length=250,required=False)
    is_multiple_choice = serializers.BooleanField(required=False)
    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class ChoiceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    question_id = serializers.UUIDField()
    text = serializers.CharField(max_length=100)
    is_correct = serializers.BooleanField(write_only=True,required=False)
    def create(self, validated_data):
        return Choice.objects.create(**validated_data)
        

class DudeSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=50)
    quiz_id = serializers.UUIDField()
    rating = serializers.FloatField()
    pass_date = serializers.DateTimeField(read_only=True)
    def create(self, validated_data):
        return Dude.objects.create(**validated_data)


