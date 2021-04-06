from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
  # /app/
  path('', views.IndexView.as_view(), name='index'),
  # /app/:question_id/
  path('<int:pk>/', views.DetailsView.as_view(), name='details'),
  # /app/:question_id/results
  path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
  # /app/:question_id/vote
  path('<int:question_id>/vote/', views.vote, name='vote')
]