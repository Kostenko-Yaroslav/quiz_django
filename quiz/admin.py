from django.contrib import admin
from django.contrib.auth.models import User

from quiz.models import Level, Question, Answer, UserResult

admin.site.register(Level)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserResult)
