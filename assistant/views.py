import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
import openai
from openai import OpenAI

openai.api_key = os.environ['OPENAI_API_KEY']

client = OpenAI()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pw = request.POST['pw']
        confirm_pw = request.POST['confirm_pw']
        if pw == confirm_pw:
            try:
                user = User.objects.create_user(username, email, pw)
                user.save()
                auth.login(request, user)
                return redirect('assistant')
            except:
                error_msg = "There was an issue creating your account."
                return render(request, 'register.html', {'error_msg': error_msg})
        else:
            error_msg = 'Please make sure both passwords match.'
            return render(request, 'register.html', {'error_msg': error_msg})
            
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pw = request.POST['pw']
        user = auth.authenticate(request, username=username, password=pw)
        if user is not None:
            auth.login(request, user)
            return redirect('assistant')
        else:
            error_msg = 'Password or Username is incorrect.'
            return render(request, 'login.html', {'error_msg': error_msg})
        
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

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


    
