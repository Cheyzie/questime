from .models import Quiz,Question,Choice,Dude
from rest_framework import serializers

class QuizSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    quiz_name = serializers.CharField(max_length=50)
    creation_date = serializers.DateTimeField(read_only=True)
    is_public = serializers.BooleanField(write_only=True)
    questions_count = serializers.SerializerMethodField()

    def get_questions_count(self, obj):
        return obj.questions.all().count()

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {'is_correct': {'write_only': True}}

class QuestionSerializer(serializers.ModelSerializer):
   
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id','wording', 'text', 'image', 'is_multiple_choice', 'choices']

class QuizDetailSerializer(serializers.ModelSerializer):
   
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_name', 'creation_date', 'is_public','questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            choices_data = question_data.pop('choices')
            question = Question.objects.create(quiz=quiz, **question_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question,**choice_data)
        return quiz
        
class DudeSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=50)
    quiz_id = serializers.UUIDField()
    rating = serializers.FloatField()
    pass_date = serializers.DateTimeField(read_only=True)
    def create(self, validated_data):
        return Dude.objects.create(**validated_data)

