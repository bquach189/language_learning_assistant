from django.shortcuts import render
from django.http import JsonResponse
import openai as ai


openai_api_key = 'sk-sxb0f2PmDVq9wkd1SESxA95whY5ZjGqghfovxVJA2cT3BlbkFJ3XJA81bbKIDCBJz1cPhfLoC6fJRY2Yl2CyXNN0VXQA'

def call_ai(msg):
    response = ai.Completion.create(
        model = 'gpt-3.5-turbo-0125',
        prompt = msg,
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    final = response.choice[0].text.strip()
    
# Create your views here.

def assistant(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        response = 'Hi there'
        return JsonResponse({'msg': msg, 'response': response})
    return render(request, 'assistant.html')