from django.shortcuts import render, redirect
from .models import User, Secret
from django.contrib import messages
from django.db.models import Count
# Create your views here.
def index(request):
  # print User.objects.all()
  return render(request, 'exam_app/index.html')

def secrets(request):
    a1 = Secret.objects.all().order_by("-created_at")[:5]
    context = {
        "secrets" : a1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    print a1
    return render(request, 'exam_app/secrets.html', context)

def like(request, id, sentby):
    print 'i liked something', id
    result = Secret.objects.like(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def delete(request, id, sentby):
    # s1 = Secret.objects.get()
    print "You wanna delete this, bruh?"
    result = Secret.objects.deleteLike(id, request.session['id'])
    if result[0] == False:
        messages.error(request, result[1])
    if sentby == "sec":
        return redirect('/secrets')
    else:
        return redirect('/popular')

def post(request):
    print request.POST['your_secret_here']
    print request.session['id']
    postData = {
        "secret" : request.POST['your_secret_here'],
        "user_id" : request.session['id'],
    }
    s1 = Secret.objects.create_secret(postData)
    for error in s1:
        message.error(request, error)
    return redirect('/secrets')

def popular(request):
    a1 = Secret.objects.annotate(num_likes=Count('likers')).order_by('-num_likes')[:5]
    context = {
        "secrets" : a1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    print a1
    return render(request, 'exam_app/popular.html', context)

def register(request):
    postdata= {
    "first_name": request.POST['first_name'],
    'last_name': request.POST['last_name'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'confirmpassword': request.POST['confirmpassword']
    }
    # get data from register form, now validate in models.Manager
    # the resultfromvalidation is just a variable store the result from validation in models.Manager
    resultfromvalidation = User.objects.register(postdata)
    print resultfromvalidation

    if len(resultfromvalidation) == 0:
        request.session['id'] = User.objects.filter(email=postdata['email'])[0].id
        request.session['name'] = postdata['first_name']
        return redirect('/secrets')
    else:
        for error in resultfromvalidation:
            messages.info(request, error)
    return redirect('/')

def login(request):
    postdata= {
    'email': request.POST['email'],
    'password': request.POST['password']
    }
    resultfromvalidation = User.objects.login(postdata)
    if len(resultfromvalidation) == 0:
        request.session['id'] = User.objects.filter(email=postdata['email'])[0].id
        request.session['name'] = User.objects.filter(email=postdata['email'])[0].first_name
        return redirect('/secrets')
    for error in resultfromvalidation:
        messages.info(request, error)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
