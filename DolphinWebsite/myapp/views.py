from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import *

from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User

# Create your views here.
def home(request):
    allproduct = Product.objects.all()
    context = {'pd': allproduct}
    return render(request, 'myapp/home.html', context)

def home2(request):
    return HttpResponse('<h1><a href="http://127.0.0.1:8000/">Hello world2</a></h1>')

def aboutUs(request):
    return render(request, 'myapp/aboutus.html')

def contact(request):
    context = {} # message to notify
    if request.method == 'POST':
        data = request.POST.copy()
        topic = data.get('topic')
        email = data.get('email')
        detail = data.get('detail')

        if (topic == '' or email == '' or detail == ''):
            context['message'] = 'Please, fill in all the contact information'
            return render(request, 'myapp/contact.html', context)
        newRecord = contactList() # create object
        newRecord.topic = topic
        newRecord.email = email
        newRecord.detail = detail
        newRecord.save() # save data

        context['message'] = 'The message has been received'

        # print(topic)
        # print(email)
        # print(detail)
        # print("---------")
    return render(request, 'myapp/contact.html', context)

def userLogin(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        password = data.get('password')

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "username or password is incorrect."

    return render(request, 'myapp/login.html', context)

def showContact(request):
    allcontact = contactList.objects.all()
    # allcontact = contactList.objects.all().order_by('-id') # reverse list
    context = {'contact': allcontact}
    return render(request, 'myapp/showcontact.html', context)

def userRegist(request):
    context = {}

    if request.method == "POST":
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        repassword = data.get('repassword')
    
        try:
            User.objects.get(username = username)
            context['message'] = "Username Duplicate"
        except:
            newuser = User()
            newuser.username = username
            newuser.first_name = firstname
            newuser.last_name = lastname
            newuser.email = email
            
            if (password == repassword):
                newuser.set_password(password)
                newuser.save()
                newprofile = Profile()
                newprofile.user = User.objects.get(username = username)
                newprofile.save()
                context['message'] = "register complete"
            else:
                context['message'] = "password or re-password is incorrect"
    return render(request, 'myapp/register.html', context)

def userProfile(request):
    context = {}
    userprofile = Profile.objects.get(user=request.user)
    context['profile'] = userprofile
    return render(request, 'myapp/profile.html', context)

def editProfile(request):
    context = {}
    if request.method == "POST":
        data = request.POST.copy()
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        current_user = User.objects.get(id=request.user.id)
        current_user.first_name = firstname
        current_user.last_name = lastname
        current_user.username = username
        current_user.email = email
        current_user.set_password(password)
        current_user.save()

        try:
            user = authenticate(username=current_user.username, 
                                password=current_user.password)
            login(request, user)
            return redirect('home-page')
        except:
            context['message'] = "edit profile fail"

    return render(request, 'myapp/editprofile.html')