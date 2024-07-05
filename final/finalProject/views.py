import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Cycle, Pc, Student, Staff, Attendance, StaffFeedback, StuFeedback, User, Comment,Post, Like
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
import os
from .chatbot.chatbot import respuesta 
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator





@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        response = respuesta(message)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



def duckBot(request):
    return render(request, 'duckBot.html')


def index(request):
    return render(request, "index.html")

@csrf_exempt
def loginStaff(request):
    if request.method == 'POST':
        username = request.POST.get('logname')
        password = request.POST.get('logpass')
        rolestaff = request.POST.get('lgStaff')
        rolest = request.POST.get('lgStudent')

        if not (username and password):
            return render(request, 'login.html', {'error_message': 'Username and password are required'})

        if not (rolestaff or rolest):
            return render(request, 'login.html', {'error_message': 'Role selection is required'})

        if rolestaff == "staff":
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})

            try:
                staff_user = Staff.objects.get(user=user)
                return render(request, "layoutstaff.html")
            except Staff.DoesNotExist:
                return render(request, 'login.html', {'error_message': 'Invalid staff credentials'})

        elif rolest == "student":
            user = authenticate(username=username, password=password)
            if user is None:
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})

            try:
                student_user = Student.objects.get(user=user)
                return render(request, "layotstu.html")
            except Student.DoesNotExist:
                return render(request, 'login.html', {'error_message': 'Invalid student credentials'})

        else:
            return render(request, 'login.html', {'error_message': 'Invalid role'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    # Cierra la sesión de manera segura
    logout(request)
    # Evita el almacenamiento en caché de la página de inicio después del cierre de sesión
    response = HttpResponseRedirect(reverse("index"))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def staffinfo(request):
    staffs = Staff.objects.all()
    return render(request, "staffinfo.html", {"staffs": staffs})

def studentinfo(request):
    students = Student.objects.all()
    return render(request, "stuinfo.html", {"students": students})

def game_view(request):
    return render(request, 'game.html')

def takeAtt(request):
    return render(request, "takeAtt.html",{
        "cycles" :Cycle.objects.all()
        })

def profile(request, user_id):
    cUser = get_object_or_404(User, pk=user_id)
    
    try:
        student = Student.objects.get(user=cUser)
        is_student = True
    except Student.DoesNotExist:
        student = None
        is_student = False
    
    try:
        staff = Staff.objects.get(user=cUser)
        is_staff = True
    except Staff.DoesNotExist:
        staff = None
        is_staff = False
    
    comments = Comment.objects.filter(profile_user=cUser).order_by('-created_at')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            if isinstance(request.user, User):
                Comment.objects.create(user=request.user, profile_user=cUser, content=content, created_at=datetime.now())
                return redirect('profile', user_id=cUser.id)
            else:
                pass
    
    context = {
        "cUser": cUser,
        "is_student": is_student,
        "student": student,
        "is_staff": is_staff,
        "staff": staff,
        "comments": comments,
    }
    
    return render(request, "profile.html", context)


def network(request):
    allposts = Post.objects.all().order_by('-id')
    paginator = Paginator(allposts, 10)
    page_number = request.GET.get('page')
    postsPage = paginator.get_page(page_number)
    liked_dict = {}

    is_student = False
    is_staff = False

    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user)
        liked_dict = {like.post.id: True for like in likes}
        
        try:
            Student.objects.get(user=request.user)
            is_student = True
        except Student.DoesNotExist:
            pass

        try:
            Staff.objects.get(user=request.user)
            is_staff = True
        except Staff.DoesNotExist:
            pass

    post_with_likes = []
    for post in postsPage:
        like_count = post.likes.count()
        post_with_likes.append({'post': post, 'likes': like_count})

    return render(request, "network.html", {
        "postsPage": postsPage,
        "liked": liked_dict,
        "posts": post_with_likes,
        "is_student": is_student,
        "is_staff": is_staff,
    })


def new_post(request):
    if request.method == "POST":
        content = request.POST.get("newpost-content")
        if content:
            if request.user.is_authenticated:
                cUser = request.user  # Use request.user directly if authenticated
                is_student = False
                is_staff = False

                # Check if the user is a student
                try:
                    student = Student.objects.get(user=cUser)
                    is_student = True
                except Student.DoesNotExist:
                    pass

                # Check if the user is staff
                try:
                    staff = Staff.objects.get(user=cUser)
                    is_staff = True
                except Staff.DoesNotExist:
                    pass
                newPost = Post(user=cUser, content=content)
                newPost.save()
                return HttpResponseRedirect(reverse('network')) 
            else:
                return render(request, "network.html", {
                    "error_message": "User must be authenticated to post."
                })
        else:
            return render(request, "network.html", {
                "error_message": "Post content cannot be empty."
            })
    else:
        return HttpResponseRedirect(reverse('network'))
    
def layoutstu(request):
    return render(request, "layoutstu.html")


def layoutstaff(request):
    return render(request, "layoutstaff.html")