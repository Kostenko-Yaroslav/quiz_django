from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from quiz.models import Level, Question, Answer, UserResult




def quiz_list(request):
    return render(request, 'quiz/quiz_list.html', {'levels': Level.objects.all()})

def quiz_detail(request, pk):
    level = Level.objects.get(pk=pk)

    return render(request, 'quiz/quiz_detail.html', {'level': level})

def quiz_submit(request, pk):
    if request.method == "POST":
        level = Level.objects.get(pk=pk)

        for question in level.question_set.all():
            answer_id = request.POST.get(str(question.id))

            answer = Answer.objects.get(pk=answer_id)

            UserResult.objects.create(user=request.user, question=question, answer=answer)

        return redirect('quiz:quiz_result', pk=pk)


def quiz_result(request, pk):
    level = Level.objects.get(pk=pk)
    result = UserResult.objects.filter(user=request.user, question__level=level)

    return render(request, 'quiz/quiz_result.html', {'result': result})