from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, "english_test_app/index.html")