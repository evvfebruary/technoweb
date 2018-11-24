from django.shortcuts import render
from django.contrib import auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views import View
from ask_evv.models import Question
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from ask_evv import paginator

# Create your views here.


class QuestionsNew(View):
    def get(self, request):
        questions = Question.objects.all()

        pagination = paginator.paginate(questions, request, key='question')
        return render(request, 'questions_list.html',
                      {
                          'questions': pagination,
                      })
        # return render(request, 'questions_list.html', context={"questions": md.Question.objects.all(),"tags":md.Tag.objects.all()})
