
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from .models import EvaluationInfo


# Create your views here.



def login(request):
    return render(request, 'users/login.html')




def logout(request):
    try:
        del request.session['userSession']
    except:
        return redirect('/')
   
    return render(request,  'users/logout.html')

    