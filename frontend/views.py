import flet as ft
from components import create_signup_view, create_login_view, create_chat_view, create_home_view


def get_view(route: str, page: ft.Page, username_input: ft.TextField, password_input: ft.TextField, password_confirm_input: ft.TextField, chat_input: ft.TextField, chat_output: ft.Column, send_message: callable, new_chat: callable):
    page.views.clear()

    if route == "/signup":
        view = create_signup_view(
            page, username_input, password_input, password_confirm_input, send_message)
    elif route == "/login":
        view = create_login_view(page, username_input,
                                 password_input, send_message)
    elif route == "/chat":
        view = create_chat_view(
            page, chat_input, chat_output, send_message, new_chat)
    else:
        view = create_home_view(page)

    page.views.append(view)
    page.update()
