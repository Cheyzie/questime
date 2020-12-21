from django.db import models
import uuid

# Create your models here.
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    creation_date = models.DateTimeField('Дата создания',auto_now_add=True)
    quiz_name = models.CharField('Название теста',max_length=50)
    is_public = models.BooleanField('Публичний тест?',default=True)
    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    quiz = models.ForeignKey(Quiz,related_name='question',on_delete=models.CASCADE)
    wording = models.CharField('Формулировка вопроса',max_length=100)
    text = models.CharField('Текст вопроса',max_length=2500, blank=True)
    image = models.CharField('Ссылка на картинку', max_length=250, blank=True)
    is_multiple_choice = models.BooleanField('Несколько ответов',default=False)

    def check_answers(self, choices_id):
        correct_choices = self.choice_set.filter(is_correct=True)
        if len(choices_id) > 0:
            if(self.is_multiple_choice):
                correct_answers = (2*sum([len(correct_choices.filter(pk=choice_id)) for choice_id in choices_id])-len(choices_id))/len(correct_choices)
                return (correct_answers if correct_answers > 0 else 0)
            else:
                if(len(correct_choices.filter(pk=choices_id[0]))>0):
                    return 1
        return 0

    def __str__(self):
        return self.wording


class Choice(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    question = models.ForeignKey(Question, related_name='choice', on_delete=models.CASCADE)
    text = models.CharField('Текст ответа',max_length=100)
    is_correct = models.BooleanField('Верный ответ',default=False)

    def __str__(self):
        return self.text

class Dude(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField('Имя',max_length=50)
    quiz_id = models.UUIDField('ID of Quiz',editable= False)
    rating = models.FloatField('Успешность чувака', editable=False)
    pass_date = models.DateTimeField('Дата прохождения',auto_now_add= True)

    def __str__(self):
        return self.name