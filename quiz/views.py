from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from quiz.models import Level, Question, Answer, UserResult


def quiz(request):
    levels = Level.objects.all()
    if request.method == "POST":
        questions = request.POST.getlist("questions")
        answers = request.POST.getlist("answers")

        for q_id, answer in zip(questions, answers):
            questions_obj = Question.objects.get(id=q_id)
            answers_obj = Answer.objects.get(id=answer)
            UserResult.objects.create(user=request.user, question=questions_obj, answer=answers_obj)


        return redirect('core:index')

    return render(request, 'quiz/quiz.html', {'levels': levels})
