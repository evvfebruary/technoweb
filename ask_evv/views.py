from django.shortcuts import render
from django.contrib import auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views import View
from ask_evv import models as md
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
# Create your views here.


class QuestionsNew(View):
    def get(self, request):
        return render(request, 'questions_list.html', context={"question":"asd"})
