import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
import openai
from openai import OpenAI
from .models import Chat, UserScore
import re

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
            error_msg = 'Please try again.'
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


def usersettings(request):
    return render(request, 'usersettings.html')

def get_previous_chats(user):
    return Chat.objects.filter(user=user).order_by('-created_at')[:10]


def create_context(previous_chats):
    context = ""
    for chat in previous_chats:
        context += f":User {chat.msg}\nAssistant: {chat.response}\n"
    return context

def get_score(response):
    match = re.search(r'Quiz Score: (\d+)/5', response)
    if match:
        return int(match.group(1))
    return None


def call_ai(context, msg, client_instance):
        prompt = context + f":User  {msg}\nAssistant:"
        response = client_instance.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            { "role": "system", "content": "You are a Language Learning Assistant Chatbot. "
                "Respond to anything language related. Politely refuse to answer anything that isn't language related."
                "When the user provides answers for the quiz, ensure you are giving answers for the most recent quiz." 
                "When providing feedback for a quiz, always count the number of correct answers out of 5, in this format: 'Quiz Score: 5/5'."
                "When asked to provide feedback, ensure you give feedback to the precise topic the user is referring to."
                "When asked to explain a grammar rule, please provide a clear and concise explanation."
                "When asked to translate a sentence, please provide the translation and a brief explanation of any nuances."
                "When practicing conversation, please provide feedback on the user's grammar at the end of the conversation."
                "When asked to provide quizzes for languages, please provide 5 questions, giving correct answers and explanations after each question."
                
                "Be polite and friendly." },
            {"role": "user", "content": prompt},       
        ],
        max_tokens = 500,
        temperature = 0.2,
    )
        final = response.choices[0].message.content
        return final.replace('\n', '\n')


def assistant(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        msg = request.POST.get('msg')
        previous_chats = get_previous_chats(request.user)
        context = create_context(previous_chats)
        response = call_ai(context, msg, client)

        score = get_score(response)
        user_score, created = UserScore.objects.get_or_create(user=request.user)

        if user_score.total_achieved_score is None:
            user_score.total_achieved_score = 0
        if user_score.total_possible_score is None:
            user_score.total_possible_score = 0

        user_score.total_achieved_score += score if score is not None else 0
        user_score.total_possible_score += 5 if score is not None else 0
        user_score.save()

        chat = Chat(user=request.user, msg=msg, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'msg': msg, 'response': response})
    return render(request, 'assistant.html',{'chats':chats})


    
