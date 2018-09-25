from django.db import models

# Пользователь – электронная почта, никнейм, пароль, аватарка, дата регистрации, рейтинг.
# Вопрос – заголовок, содержание, автор, дата создания, теги, рейтинг.
# Ответ – содержание, автор, дата написания, флаг правильного ответа, рейтинг.
# Тег – слово тега.
from django.utils import timezone

# class Profile(models.Model):
#     :ToDo


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    # author must be foreign key :ToDo
    # tags :ToDo

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # author must be foreign key :ToDo

    def __str__(self):
        return str("[" + str(self.id) + "]" + self.title)


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title is other
