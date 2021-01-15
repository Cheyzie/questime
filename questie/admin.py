from django.contrib import admin
from .models import Quiz, Question, Choice, Dude, Image, Result
# Register your models here.


class ResultInline(admin.TabularInline):
    model = Result
    extra = 2


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'wording', 'is_multiple_choice']
    inlines = [ChoiceInline]
    list_filter = ['quiz']

class DudeAdmin(admin.ModelAdmin):
    list_display=['name',]
    inlines = [ResultInline]


admin.site.register(Quiz)
admin.site.register(Image)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Dude, DudeAdmin)