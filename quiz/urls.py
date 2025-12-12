from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('quiz_list', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/quiz_submit', views.quiz_submit, name='quiz_submit'),
    path('quiz/<int:pk>/quiz_result', views.quiz_result, name='quiz_result'),
]