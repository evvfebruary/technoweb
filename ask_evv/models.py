import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
# Пользователь – электронная почта, никнейм, пароль, аватарка, дата регистрации, рейтинг.
# Вопрос – заголовок, содержание, автор, дата создания, теги, рейтинг.
# Ответ – содержание, автор, дата написания, флаг правильного ответа, рейтинг.
# Тег – слово тега.


# Extended user profile ( with awesome avatar img )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar_imgs')
    info = models.TextField()

    def __str__(self):
        return str(self.user.username)+"[{}]".format(self.user_id)


# Tags part

class TagManager(models.Manager):

    def populars(self, size):
        return self.annotate(cnt=Count('question')).order_by('-cnt').all()[:size]


class Tag(models.Model):
    GREEN = 'success'
    DBLUE = 'primary'
    BLACK = 'default'
    RED = 'danger'
    LBLUE = 'info'
    COLORS = (
        ('GR', GREEN),
        ('DB', DBLUE),
        ('B', BLACK),
        ('RE', RED),
        ('BL', LBLUE)
    )

    title = models.CharField(max_length=30,
                             verbose_name='Название')
    color = models.CharField(max_length=2,
                             choices=COLORS,
                             default=BLACK,
                             verbose_name='Цвет')

    objects = TagManager()

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return self.title is other


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

    def get_ordering(self, request):
        return ['title']

# Tags end


# Questions part

class QuestionQuerySet(models.QuerySet):
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author().with_tags()

    def with_tags(self):
        return self.prefetch_related('tags')

    def with_answers(self):
        self.prefetch_related('answer_set')
        self.prefetch_related('answer_set__author')
        return self.prefetch_related('answer_set__author__profile')

    def with_answers_count(self):
        return self.annotate(answers=Count('answer__id', distinct=True))

    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    def populars(self):
        return self.order_by('-likes')

    def with_date_greater(self, date):
        return self.filter(date__gt=date)


class QuestionManager(models.Manager):
    # custom query set
    def get_queryset(self):
        res = QuestionQuerySet(self.model, using=self._db)
        return res.with_answers_count().with_author().with_tags()

    # list of new questions
    def list_new(self):
        return self.order_by('-date')

    # list of hot questions
    def list_hot(self):
        return self.order_by('-likes')

    # list of questions with tag
    def list_tag(self, tag):
        return self.filter(tags=tag)

    # single question
    def get_single(self, _id):
        res = self.get_queryset()
        return res.with_answers().get(pk=_id)

    # best questions
    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset() \
            .order_by_popularity() \
            .with_date_greater(week_ago)


class Question(models.Model):

    class Meta:
        db_table = 'questions'
        ordering = ['-date']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def get_url(self):
        return reverse('question', kwargs={'id': self.id})

    def get_prettify_title(self):
        title_formatted_text = self.title[:80] + "..." if len(self.title) > 80 else self.title
        return title_formatted_text

    def __str__(self):
        return "[" + str(self.id) + "]" + self.title


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date',)
    search_fields = ('title', 'text',)
    readonly_fields = ('likes',)

    def get_ordering(self, request):
        return ['-date', 'title']

    def get_list_filter(self, request):
        return ['author', 'tags']

# Questions end


# Answers part

class AnswerQuerySet(models.QuerySet):

    def with_author(self):
        return self.select_related('author').select_related('author__profile')

    def with_question(self):
        return self.select_related('question')

    def order_by_popularity(self):
        return self.order_by('-likes')

    def with_date_greater(self, date):
        return self.filter(date__gt=date)


class AnswerManager(models.Manager):
    def get_queryset(self):
        res = AnswerQuerySet(self.model, using=self._db)
        return res.with_author()

    def get_best(self):
        week_ago = timezone.now() + datetime.timedelta(-7)
        return self.get_queryset() \
            .order_by_popularity() \
            .with_date_greater(week_ago)


class Answer(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = AnswerManager()

    def mark_correct(self, user = None):
        if user is not None and self.question.author.id != user.id:
            raise Exception("Вы не автор вопроса!")
        self.correct = True
        self.save()

    def __str__(self):
        return "[{}] {}".format(self.id, self.title)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'author', 'date', 'correct')
    search_fields = ('text',)
    readonly_fields = ('likes',)

    def get_ordering(self, request):
        return ['-date']

    def get_list_filter(self, request):
        return ['author', 'correct']

