from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'myapp/home.html')

def home2(request):
    return HttpResponse('<h1><a href="http://127.0.0.1:8000/">Hello world2</a></h1>')

def aboutUs(request):
    return render(request, 'myapp/aboutus.html')