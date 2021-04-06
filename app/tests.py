import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.
class QuestionModelTest(TestCase):

  def test_was_published_recently_with_future_question(self):
    # testa se foi publicado recentemente e retorna falso
    # para datas no futuro
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertIs(future_question.was_published_recently(), False)

  def test_was_published_recently_with_old_question(self):
    # testa se a função retorna falsa para questões cujo pub_date
    # é maior que um dia
    time = timezone.now() - datetime.timedelta(days=1, seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(), False)

  def test_was_published_recently_with_recent_question(self):
    # testa se a função retorna True para as questões cujo pub_date
    # está no último dia
    time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
  # cria uma questão com um dado 'question_text' e publica
  # o offset do número de dias até agora (negativo para
  # questões publicadas já publicadas, positivo para questões
  # estão próximas de acontecer)
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexView(TestCase):
  def test_no_questions(self):
    # se não existir questões, uma msg apropiada é mostrada
    response = self.client.get(reverse('app:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['lastest_question_list'], [])

  def test_past_question(self):
    # Questão com o pub_date no passado são mostrados na index
    create_question(question_text="Past question.", days=-30)
    response = self.client.get(reverse('app:index'))
    self.assertQuerysetEqual(
      response.context['lastest_question_list'],
      ['<Question: Past question.>']
    )

  def test_future_question(self):
    # Questões com datas futuras não são mostradas na index
    create_question(question_text="Past question.", days=-30)
    create_question(question_text="Future question.", days=30)
    response = self.client.get(reverse('app:index'))
    self.assertQuerysetEqual(
        response.context['lastest_question_list'],
        ['<Question: Past question.>']
    )

  def test_two_past_questions(self):
    # Multiplas questôes mostradas na index
    create_question(question_text="Past question 1.", days=-30)
    create_question(question_text="Past question 2.", days=-5)
    response = self.client.get(reverse('app:index'))
    self.assertQuerysetEqual(
        response.context['lastest_question_list'],
        ['<Question: Past question 2.>', '<Question: Past question 1.>']
    )

class QuestionDetailViewTest(TestCase):
  def test_future_question(self):
    # verifica se uma questão não pubicada recebe o 404
    future_question = create_question(question_text='Future question.',
                                      days=5)
    url = reverse('app:details', args=(future_question.id,))
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)

  def test_past_question(self):
    # verifica se somente questões publicadas aparecem
    past_question = create_question(question_text='Past question.',
                                    days=-5)
    url = reverse('app:details', args=(past_question.id,))
    response = self.client.get(url)
    self.assertContains(response, past_question.question_text)