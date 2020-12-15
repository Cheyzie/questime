from django.urls import path
from .views import QuizzesView, QuizView, AnswerView

app_name = 'questie'

urlpatterns = [
    path('', QuizzesView.as_view()),
    path('<uuid:pk>/', QuizView.as_view()),
    path('<uuid:pk>/answer/', AnswerView.as_view())
]