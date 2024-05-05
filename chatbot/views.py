# chatbot/views.py

import openai
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from ninja import Router
from .models import User
from .schemas import SignUpSchema, LoginSchema, ChatInput, ChatOutput

router = Router()
openai.api_key = ""


@router.post("/signup")
def signup(request, data: SignUpSchema):
    form = UserCreationForm({
        'username': data.username,
        'password1': data.password1,
        'password2': data.password2,
    })
    if form.is_valid():
        user = form.save()
        login(request, user)
        return {"success": True, "message": "User registered successfully!"}
    else:
        return {"success": False, "errors": form.errors}


@router.post("/login")
def user_login(request, data: LoginSchema):
    user = authenticate(request, username=data.username,
                        password=data.password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True, "message": "Logged in successfully!"})
    else:
        return JsonResponse({"success": False, "message": "Invalid credentials"})


@router.post("/chat", response=ChatOutput)
def chat(request, data: ChatInput):
    if not request.user.is_authenticated:
        return {"response": "You must be logged in to chat."}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": data.message}],
        )
        chat_response = response.choices[0].message['content']
        return {"response": chat_response}
        # return {"response": "chat_response"}
    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}


@router.get("/logout")
def user_logout(request):
    logout(request)
    return JsonResponse({"success": True, "message": "Logged out successfully!"})
