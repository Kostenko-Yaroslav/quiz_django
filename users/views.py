from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Avg
from quiz.models import Attempt
from .models import UserAchievement

class CreateUserView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

@login_required
def profile_view(request):
    user = request.user

    attempts = Attempt.objects.filter(user=user).order_by("-date")
    total_attempts = attempts.count()

    avg_accuracy = attempts.aggregate(avg=Avg("percentage"))["avg"]
    avg_accuracy = round(avg_accuracy, 1) if avg_accuracy else 0

    achievements = UserAchievement.objects.filter(user=user)

    return render(request, "users/profile.html", {
        "user": user,
        "attempts": attempts,
        "total_attempts": total_attempts,
        "avg_accuracy": avg_accuracy,
        "achievements": achievements,
    })
