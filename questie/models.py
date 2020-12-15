from django.db import models

# Create your models here.
class Quiz(models.Model):
    creation_date = models.DateTimeField('Дата создания',auto_now_add=True)
    quiz_name = models.CharField('Название теста',max_length=50)

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    wording = models.CharField('Формулировка вопроса',max_length=100)
    text = models.CharField('Текст вопроса',max_length=250)
    image = models.CharField('Ссылка на картинку', max_length=100)
    is_multiple_choice = models.BooleanField('Несколько ответов',default=False)

    def __str__(self):
        return self.wording


class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text = models.CharField('Текст ответа',max_length=100)
    is_correct = models.BooleanField('Верный ответ',default=False)

    def __str__(self):
        return self.text

class Dude(models.Model):
    name = models.CharField('Имя',max_length=50)
    quiz_id = models.IntegerField('ID of Quiz',editable= False)
    rating = models.FloatField('Успешность чувака')
    pass_date = models.DateTimeField('Дата прохождения',auto_now_add= True)

    def __str__(self):
        return self.name