from django.http import HttpResponse
from django.shortcuts import render

# Index page
def index(request):
    return HttpResponse('Authentication index endpoint')

# Register
def register(request):
    return HttpResponse('Register user')

# Login
def login(request):
    return HttpResponse('Login user')
