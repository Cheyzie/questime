from django.db import models
import uuid
import os
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password


# Create your models here.


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    creation_date = models.DateTimeField('Дата создания', auto_now_add=True)
    quiz_name = models.CharField('Название теста', max_length=50)
    is_public = models.BooleanField('Публичний тест?', default=True)

    def __str__(self):
        return self.quiz_name


class Image(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    picture = models.ImageField('Картинка', upload_to='images', blank=False, null=False)
    editing_key = models.CharField(max_length=16, default=make_password(''), blank=True)

    def __str__(self):
        return self.picture.url


class Question(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    wording = models.CharField('Формулировка вопроса', max_length=100)
    text = models.CharField('Текст вопроса', max_length=2500, blank=True)
    image = models.ForeignKey(Image, related_name='questions', on_delete=models.SET_NULL, blank=True, null=True)
    is_multiple_choice = models.BooleanField('Несколько ответов', default=False)

    def check_answers(self, choices_id):
        correct_choices = self.choices.filter(is_correct=True)
        if len(choices_id) > 0:
            if self.is_multiple_choice:
                correct_answers = (2*sum([len(correct_choices.filter(pk=choice_id)) for choice_id in choices_id]) -
                                   len(choices_id))/len(correct_choices)
                return correct_answers if correct_answers > 0 else 0
            else:
                if len(correct_choices.filter(pk=choices_id[0])) > 0:
                    return 1
        return 0

    def __str__(self):
        return self.wording


class Choice(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField('Текст ответа', max_length=100)
    is_correct = models.BooleanField('Верный ответ', default=False)

    def __str__(self):
        return self.text


class Dude(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField('Имя', max_length=50)
    editing_key = models.CharField(max_length=16, default=make_password('')[-16:], blank=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    dude = models.ForeignKey(Dude, related_name='results', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='results', editable=False, on_delete=models.CASCADE)
    rating = models.FloatField('Успешность Сани')
    pass_date = models.DateTimeField('Дата прохождения', auto_now_add=True)



@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding 'MediaFile' object is deleted.
    """
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding 'Image' object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Image.objects.get(pk=instance.pk).picture
    except Image.DoesNotExist:
        return False

    new_file = instance.picture
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
