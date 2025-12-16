from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from quiz.models import Level, Question, Answer, UserResult, Attempt
from users.models import UserProfile, Achievement, UserAchievement


def is_level_unlocked(user, level):
    if level.order == 1:
        return True

    previous_level = Level.objects.filter(order=level.order - 1).first()
    if not previous_level:
        return False

    return Attempt.objects.filter(
        user=user,
        level=previous_level
    ).exists()

@login_required
def quiz_list(request):
    levels = Level.objects.order_by("order")

    levels_with_access = [
        {
            "level": level,
            "unlocked": is_level_unlocked(request.user, level)
        }
        for level in levels
    ]

    return render(request, "quiz/quiz_list.html", {
        "levels": levels_with_access
    })

@login_required
def quiz_detail(request, pk):
    level = get_object_or_404(Level, pk=pk)

    if not is_level_unlocked(request.user, level):
        return redirect("quiz:quiz_list")

    return render(request, "quiz/quiz_detail.html", {
        "level": level
    })

@login_required
def quiz_submit(request, pk):
    if request.method != "POST":
        return redirect("quiz:quiz_list")

    level = get_object_or_404(Level, pk=pk)
    questions = level.question_set.all()

    total = questions.count()
    correct = 0

    attempt = Attempt.objects.create(
        user=request.user,
        level=level,
        total_question=0,
        correct_answers=0,
        percentage=0
    )

    for question in questions:
        answer_id = request.POST.get(str(question.id))
        if not answer_id:
            continue

        answer = get_object_or_404(Answer, pk=answer_id)
        is_correct = answer.is_correct

        if is_correct:
            correct += 1

        UserResult.objects.create(
            attempt=attempt,
            question=question,
            answer=answer,
            is_correct=is_correct
        )

    percentage = round((correct / total) * 100, 2) if total > 0 else 0

    attempt.total_question = total
    attempt.correct_answers = correct
    attempt.percentage = percentage
    attempt.save()

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    earned_xp = correct * 10
    profile.xp += earned_xp
    profile.save()

    if Attempt.objects.filter(user=request.user).count() == 1:
        ach = Achievement.objects.filter(code="first_attempt").first()
        if ach:
            UserAchievement.objects.get_or_create(
                user=request.user,
                achievement=ach
            )

    if percentage == 100:
        ach = Achievement.objects.filter(code="perfect_score").first()
        if ach:
            UserAchievement.objects.get_or_create(
                user=request.user,
                achievement=ach
            )

    return redirect("quiz:quiz_result", pk=attempt.pk)

@login_required
def quiz_result(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk, user=request.user)
    results = UserResult.objects.filter(attempt=attempt)

    return render(request, "quiz/quiz_result.html", {
        "attempt": attempt,
        "results": results
    })
