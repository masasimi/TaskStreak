from django.contrib.auth import authenticate, models, login, logout
from django.db import IntegrityError

from django.views.decorators.csrf import requires_csrf_token

from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render

import datetime
from django.utils import timezone
from django.utils.timezone import localtime

from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login/')

    tasks = Task.objects.filter(user=request.user).order_by("-currentStreak")

    now = localtime(timezone.now())
    yesterday = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterdayEnd = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)
    for task in tasks:
        if localtime(task.lastDate) < yesterday:
            task.currentStreak = 0
        if task.currentStreak and yesterdayEnd < localtime(task.lastDate):
            task.isDoneToday = True
        else :
            task.isDoneToday = False
        task.save()
        
    return render(
        request,
        'todo_list/todo_list.html',
        {'username': request.user.username, 'tasks': tasks}
    )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'todo_list/login.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404('Username or password is not set.')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return render(request, 'todo_list/login.html', {'error_message': 'Incorrect username or password.'})

    login(request, user)
    return HttpResponseRedirect('../')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect('../login/')


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return render(request, 'todo_list/register.html')
    elif request.method != 'POST':
        raise Http404('Request method is not GET or POST.')

    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError as e:
        raise Http404(e)

    try:
        user = models.User.objects.create_user(username=username, password=password)
    except IntegrityError as e:
        raise Http404(f'Username {username} is already registered. Please register another username.')

    login(request, user)
    return HttpResponseRedirect('../')


def check_task_request(request: HttpRequest) -> None:
    if request.method != 'POST':
        raise Http404('Request method is not POST.')

    user=request.user
    if not user.is_authenticated:
        raise Http404('User is not authenticated.')


def create_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    title = request.POST.get('title')
    description = request.POST.get('description')
    if title is None:
        Http404('Task name is not set.')

    now = timezone.now()
    #yesterday = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    task = Task(user=request.user, title=title, description=description, lastDate=now)
    task.save()
    return HttpResponseRedirect('../../')


def update_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    title = request.POST.get('title')
    description = request.POST.get('description')
    if id is None or title is None:
        Http404('Task id or name is not set.')

    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be edited.")

    task.title = title
    task.description = description
    task.save()
    return HttpResponseRedirect('../../')


def done_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')

    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be done.")

    now = localtime(timezone.now())
    yesterday = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterdayEnd = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    if localtime(task.lastDate) <= yesterdayEnd or task.isDoneToday == False:
        task.streakSum += 1
        task.currentStreak += 1

        if task.currentStreak > task.longestStreak:
            task.longestStreak = task.currentStreak
    

    task.isDoneToday = True
    task.lastDate = now
    task.save()
    return HttpResponseRedirect('../../')


def delete_task(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')

    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be edited.")

    task.delete()
    return HttpResponseRedirect('../../')

def new_form_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login/')

    return render(
        request,
        'todo_list/todo_new_form.html',
        {'username': request.user.username}
    )

def edit_form_view(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')

    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be edited.")

    return render(
        request,
        'todo_list/todo_edit_form.html',
        {'username': request.user.username, 'task': task}
    )


def detail_view(request: HttpRequest) -> HttpResponse:
    check_task_request(request=request)

    id_ = request.POST.get('id')
    if id is None:
        Http404('Task id is not set.')

    task = Task.objects.get(pk=id_)
    if task.user != request.user:
        raise Http404("Another user's task can't be seen.")

    now = localtime(timezone.now())
    yesterday = (now - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yesterdayEnd = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    if yesterdayEnd < localtime(task.lastDate) and task.isDoneToday == False:
        isNotyet = True
    else:
        isNotyet = False
    lastDate = localtime(task.lastDate).strftime("%Y-%m-%d")


    return render(
        request,
        'todo_list/todo_detail.html',
        {'username': request.user.username, 'task': task, 'lastDate' : lastDate , 'isNotyet' : isNotyet}
    )

@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
