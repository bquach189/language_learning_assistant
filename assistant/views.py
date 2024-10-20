from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def assistant(request):
    if request.method == 'POST':
        message = request.POST.get('msg')
        response = 'Hi there'
        return JsonResponse
    return render(request, 'assistant.html')