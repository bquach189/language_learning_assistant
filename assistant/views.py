import os
from django.shortcuts import render
from django.http import JsonResponse
import openai
from openai import OpenAI

openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()

def call_ai(msg, client_instance):
        response = client_instance.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            { "role": "system", "content": "You are a Language Learning Assistant Chatbot." },
            {"role": "user", "content": msg},       
        ],
        max_tokens = 200,
        temperature = 2,
    )
        final = response.choices[0].message.content
        return final
# Create your views here.

def assistant(request):
    if request.method == 'POST':
        msg = request.POST.get('msg')
        response = call_ai(msg, client)
        return JsonResponse({'msg': msg, 'response': response})
    return render(request, 'assistant.html')