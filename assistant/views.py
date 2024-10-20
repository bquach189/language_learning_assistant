from django.shortcuts import render

# Create your views here.

def assistant(request):
    return render(request, 'assistant.html')