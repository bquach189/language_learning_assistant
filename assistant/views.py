import os
from django.shortcuts import render
from django.http import JsonResponse
<<<<<<< HEAD
from django.contrib import auth
=======
>>>>>>> b6cda64df0d199f5aa1f697122370cf2d0528f63
import openai
from openai import OpenAI

openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()

<<<<<<< HEAD
def register(request):
    if request.method == 'POST':
        user = request.POST.get('username', '')
        email = request.POST.get('email', '')
        pw = request.POST.get('pw', '')
        confirm_pw = request.POST.get('confirm_pw', '')
        if pw == confirm_pw:
            try:
                pass
            except:
                pass
        else:
            error_msg = 'Please make sure both passwords match.'
            return render(request, 'register.html', {'error_msg': error_msg})
            
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)

=======
>>>>>>> b6cda64df0d199f5aa1f697122370cf2d0528f63
def call_ai(msg, client_instance):
        response = client_instance.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            { "role": "system", "content": "You are a Language Learning Assistant Chatbot." },
            {"role": "user", "content": msg},       
        ],
        max_tokens = 200,
        temperature = 0.2,
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


    
