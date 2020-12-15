from django.urls import path
from .views import QuizView, QuizDetailView

app_name = 'questie'

urlpatterns = [
    path('', QuizView.as_view()),
    path('<int:pk>/', QuizDetailView.as_view())
]