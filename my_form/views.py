from django.shortcuts import render

def register(request):
    return render(request, "register.html")

def apply(request):
    return render(request, "apply.html")