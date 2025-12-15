
from django.shortcuts import render, redirect


from quiz.models import Level, Question, Answer, UserResult, Attempt


def quiz_list(request):
    return render(request, 'quiz/quiz_list.html', {'levels': Level.objects.all()})

def quiz_detail(request, pk):
    level = Level.objects.get(pk=pk)

    return render(request, 'quiz/quiz_detail.html', {'level': level})

def quiz_submit(request, pk):
    if request.method == "POST":
        level = Level.objects.get(pk=pk)

        question = level.question_set.all()
        total = question.count()
        correct = 0

        attempt = Attempt.objects.create(
            user = request.user,
            level = level,
            total_question = 0,
            correct_answers = 0,
            percentage = 0
        )

        for question in level.question_set.all():
            answer_id = request.POST.get(str(question.id))

            answer = Answer.objects.get(pk=answer_id)

            is_correct = answer.is_correct

            if is_correct == True:
                correct += 1

            UserResult.objects.create(attempt=attempt, question=question, answer=answer, is_correct=is_correct)

        attempt.percentage = correct / total * 100
        attempt.total_question = total
        attempt.correct_answers = correct
        attempt.save()

        return redirect('quiz:quiz_result', pk=attempt.pk)


def quiz_result(request, pk):
    attempt = Attempt.objects.get(pk=pk, user=request.user)
    result = UserResult.objects.filter(attempt=attempt)

    return render(request, 'quiz/quiz_result.html', {'result': result, 'attempt': attempt},)