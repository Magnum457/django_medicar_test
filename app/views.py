from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
  template_name = 'app/index.html'
  context_object_name = 'lastest_question_list'

  def get_queryset(self):
    # Retorna as 5 últimas questões publicadas
    return Question.objects.filter(
      pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]

class DetailsView(generic.DetailView):
  model = Question
  template_name = 'app/details.html'

  def get_queryset(self):
    # Exclui qualquer pergunta que não foi publicada
    return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):  
  model = Question
  template_name = 'app/results.html'

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # Volta para a tela de opções
    return render(request, 'app/details.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    # Sempre redirecione um HttpResponseRedirect depois de lidar
    # com POST data. Isso previne que os dados sejam postados 2 vezes
    # se o usuário clicar no botão 2 vezes.
    return HttpResponseRedirect(reverse('app:results',
                                        args=(question.id, )))