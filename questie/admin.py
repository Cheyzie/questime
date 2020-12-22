from django.contrib import admin
from .models import Quiz, Question, Choice, Dude
# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'wording', 'is_multiple_choice']
    inlines = [ChoiceInline]
    list_filter = ['quiz']

class DudeAdmin(admin.ModelAdmin):
    list_display=['name', 'rating', 'pass_date']
    list_filter = ['pass_date']



admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Dude, DudeAdmin)