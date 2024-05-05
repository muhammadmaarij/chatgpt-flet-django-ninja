# chatbot/schemas.py

# chatbot/schemas.py

from ninja import Schema


class SignUpSchema(Schema):
    username: str
    password1: str
    password2: str


class LoginSchema(Schema):
    username: str
    password: str


class ChatInput(Schema):
    message: str


class ChatOutput(Schema):
    response: str
