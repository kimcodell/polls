from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic

# Create your views here.


# def index(req):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(output)
#
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # template = loader.get_template('polls/index.html')
#     # return HttpResponse(template.render(context, req))
#
#     return render(req, 'polls/index.html', context)
#
#
# def detail(req, question_id):
#     # return HttpResponse('question detail %s' % question_id)
#
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(req, 'polls/detail.html', {'question': question})
#
#
# def results(req, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(req, 'polls/result.html', {'question': question})
#
#
def vote(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        if len(req.POST.getlist('choice')) == 0:
            raise Exception("선택을 하지 않았습니다.")
        selected_choices = question.choice_set.filter(pk__in=req.POST.getlist('choice'))
    except(KeyError, Choice.DoesNotExist):
        return render(req, 'polls/detail.html', {'question': question, 'error_message': '선택을 하지 않았습니다'})
    except Exception:
        return render(req, 'polls/detail.html', {'question': question, 'error_message': '선택을 하지 않았습니다'})
    else:
        for choice in selected_choices:
            choice.votes += 1
            choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'
