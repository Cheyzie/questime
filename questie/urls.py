from django.urls import path
from .views import QuizzesView, QuizView, ResultsView, ImagesView,\
    ImageView, DudesView, DudeView

app_name = 'questie'

urlpatterns = [
    path('', QuizzesView.as_view()),
    path('<uuid:pk>/', QuizView.as_view()),
    path('<uuid:pk>/answer/', ResultsView.as_view()),
    path('dude', DudesView.as_view()),
    path('dude/<uuid:pk>', DudeView.as_view()),
    path('image', ImagesView.as_view()),
    path('image/<uuid:pk>', ImageView.as_view())
]