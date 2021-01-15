from .models import Quiz,Question,Choice,Dude,Image, Result
from rest_framework import serializers
import uuid
import re

class QuizSerializer(serializers.ModelSerializer):

    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Quiz
        fields = ['id', 'quiz_name', 'creation_date', 'is_public','questions_count']

    def get_questions_count(self, obj):
        return obj.questions.all().count()

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

class ImageSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField()

    class Meta:
        model=Image
        fields=['id', 'picture']

class ImageRelatedSerializer(ImageSerializer):

    def to_internal_value(self, data):
        try:
            image = self.Meta.model.objects.get(id=data)
        except self.Meta.model.DoesNotExist:
            return None
        return self.Meta.model.objects.get(id=data)

class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']
        extra_kwargs = {'is_correct': {'write_only': True}}

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)
    image = ImageRelatedSerializer(required=False)

    def to_internal_value(self, data):
        correct_choices = len([choice for choice in data.get('choices') if str(choice.get('is_correct')).lower() == 'true'])
        if correct_choices>1 and not 'is_multiple_choice' in data:
            data['is_multiple_choice'] = True
        if data.get('image', None) == '':
            data.pop('image')
        return super(QuestionSerializer, self).to_internal_value(data)
    
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
        
class DudeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dude
        fields = ['id', 'name']
    
    def create(self, validated_data):
        return Dude.objects.create(**validated_data)


class QuizRelatedSerializer(QuizSerializer):

    def to_internal_value(self, data):
        try:
            image = self.Meta.model.objects.get(id=data)
        except self.Meta.model.DoesNotExist:
            return None
        return self.Meta.model.objects.get(id=data)


class DudeRelatedSerializer(DudeSerializer):
    
    def to_internal_value(self, data):
        try:
            image = self.Meta.model.objects.get(id=data)
        except self.Meta.model.DoesNotExist:
            return None
        return self.Meta.model.objects.get(id=data)


class ResultSerializer(serializers.ModelSerializer):
    dude = DudeRelatedSerializer(many=False)
    quiz = QuizRelatedSerializer(many=False)
    class Meta:
        model = Result
        fields = ['dude', 'quiz', 'rating', 'pass_date']
        read_only_fields=['pass_date']

    def create(self, validated_data):
        return Result.objects.create(**validated_data)


class DudeDetailSerializer(serializers.ModelSerializer):
    results = ResultSerializer(many=True)
    class Meta:
        model = Dude
        fields = ['id', 'name', 'results']

