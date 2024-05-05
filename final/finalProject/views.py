from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Cycle, Pc, Student, Staff, Attendance, StaffFeedback, StuFeedback

def index(request):
    return render(request,"index.html")

def login(request):
    return render(request, "login.html")