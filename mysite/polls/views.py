from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import Question, Vote, Choice

def log_in(request):
    if request.method == 'GET':
        return render(request, 'polls/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            messages.warning(request, "The e-mail address and/or password you specified are not correct.")
            return render(request, 'polls/login.html')


def log_out(request):
    logout(request)
    messages.success(request, "You have successfully been logged out")
    return HttpResponseRedirect(reverse('polls:index'))


def registration(request):
    if request.method == 'GET':
        return render(request, 'polls/registration.html')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        errors = {}

        if not username:
            errors['username'] = 'Please choose a username.'

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = 'Enter a valid email address.'

        if not password1:
            errors['password1'] = 'Password is required.'
        
        if password1 != password2:
            errors['password2'] = 'Passwords don\'t match.'

        if errors:
            context = {'errors': errors, 'username': username, 'email': email}
            return render(request, 'polls/registration.html', context)

        user = User.objects.create_user(username, email, password1)
        login(request, user)

        return HttpResponseRedirect(reverse('polls:index'))


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'GET':
        context = {'question': question}
        if (
            request.user.is_authenticated
            and Vote.objects.filter(
                user=request.user, choice__in=question.choices.all()
            ).exists()
        ):
            return render(request, 'polls/results.html', context)
        else:
            return render(request, 'polls/detail.html', context)

    if request.method == 'POST':
        if 'choice' not in request.POST:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice."
            })
        if not request.user.is_authenticated:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You're not authorized."
            })

        choice_id = request.POST['choice']
        selected_choice = get_object_or_404(question.choices, pk=choice_id)
        Vote.objects.create(choice=selected_choice, user=request.user)
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )


def vote_again(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)


def add_polls(request):
    if request.method == 'POST':
        question_text = request.POST['question_text']
        choices = request.POST.getlist('choices')
        question = Question.objects.create(question_text=question_text)
        for choice_text in choices:
            Choice.objects.create(choice_text=choice_text, question=question)
        messages.success(request, "Question added")
        return HttpResponseRedirect(reverse('polls:index'))