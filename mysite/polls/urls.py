from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('addpolls/', views.add_polls, name='addpolls'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/vote_again/', views.vote_again, name='vote_again'),
]

