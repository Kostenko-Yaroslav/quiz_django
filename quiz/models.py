from django.contrib.auth.models import User
from django.db import models

class Level(models.Model):
    name = models.CharField(max_length=100)
    theme = models.CharField(max_length=100, blank=True)
    complexity = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer


class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    total_question = models.IntegerField()
    correct_answers = models.IntegerField()
    percentage = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.level.name} | {self.percentage}%"

class UserResult(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question.question_text} → {self.answer.answer}"





