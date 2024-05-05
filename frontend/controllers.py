import requests
import flet as ft
from views import get_view


class ChatAppController:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/"
        self.user_token = None
        self.username = None
        self.chats = []
        self.selected_chat_index = 0
        self.sidebar_column = None

    def handle_route_change(self, route: str, page: ft.Page):
        username_input = ft.TextField(
            label="Username", width=300, autofocus=True)
        password_input = ft.TextField(
            label="Password", password=True, width=300)
        password_confirm_input = ft.TextField(
            label="Confirm Password", password=True, width=300)
        chat_input = ft.TextField(label="Message", expand=True)
        chat_output = ft.Column(auto_scroll=True, expand=True)
        sidebar_controls = []

        def update_sidebar():
            self.sidebar_column.controls.clear()
            for index, chat in enumerate(self.chats):
                self.sidebar_column.controls.append(
                    ft.TextButton(
                        text=chat["name"],
                        on_click=lambda e, index=index: select_chat(index),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5))
                    )
                )
            self.sidebar_column.controls.append(
                ft.ElevatedButton("New Chat", on_click=new_chat)
            )
            self.sidebar_column.update()

        def select_chat(index):
            self.selected_chat_index = index
            chat_output.controls.clear()
            chat_output.controls.extend(
                self.chats[self.selected_chat_index]["messages"])
            chat_output.auto_scroll = True
            page.update()

        def new_chat(e):
            chat_name = f"Chat {len(self.chats) + 1}"
            self.chats.append({"name": chat_name, "messages": []})
            update_sidebar()
            select_chat(len(self.chats) - 1)

        def sign_up(e):
            self.username = username_input.value
            password1 = password_input.value
            password2 = password_confirm_input.value
            response = requests.post(
                self.base_url + "signup", json={"username": self.username, "password1": password1, "password2": password2})
            result = response.json()
            if result.get("success"):
                page.session.set(
                    "user_token", response.cookies.get("sessionid"))
                page.snack_bar = ft.SnackBar(
                    ft.Text("Sign up successful!"), open=True)
                page.go("/chat")
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error: {result.get('errors')}"), open=True)
                page.update()

        def login(e):
            self.username = username_input.value
            password = password_input.value
            response = requests.post(
                self.base_url + "login", json={"username": self.username, "password": password})
            result = response.json()
            if result.get("success"):
                page.session.set(
                    "user_token", response.cookies.get("sessionid"))
                page.snack_bar = ft.SnackBar(
                    ft.Text("Login successful!"), open=True)
                page.go("/chat")
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Invalid credentials"), open=True)
                page.update()

        def send_message(e):
            user_token = page.session.get("user_token")
            if user_token is None:
                page.snack_bar = ft.SnackBar(
                    ft.Text("You must be logged in to chat."), open=True)
                page.update()
                return

            user_message = chat_input.value
            user_message_text = ft.Text(f"{self.username}: {user_message}")
            self.chats[self.selected_chat_index]["messages"].append(
                user_message_text)
            chat_output.controls.append(user_message_text)
            chat_output.controls.append(ft.Divider())
            chat_output.auto_scroll = True
            page.update()

            try:
                response = requests.post(
                    self.base_url + "chat", json={"message": user_message}, cookies={"sessionid": user_token})
                result = response.json()
                bot_message_text = ft.Text(
                    f"ChatGPT: {result.get('response')}")
                self.chats[self.selected_chat_index]["messages"].append(
                    bot_message_text)
                chat_output.controls.append(bot_message_text)
                chat_output.controls.append(ft.Divider())
            except requests.exceptions.JSONDecodeError as err:
                error_text = ft.Text(
                    "Error: Unable to decode server response.")
                self.chats[self.selected_chat_index]["messages"].append(
                    error_text)
                chat_output.controls.append(error_text)
                chat_output.controls.append(ft.Divider())
            except Exception as e:
                error_text = ft.Text(f"An error occurred: {str(e)}")
                self.chats[self.selected_chat_index]["messages"].append(
                    error_text)
                chat_output.controls.append(error_text)
                chat_output.controls.append(ft.Divider())
            chat_output.auto_scroll = True
            page.update()

        get_view(route, page, username_input, password_input,
                 password_confirm_input, chat_input, chat_output, send_message, new_chat)


controller = ChatAppController()
initial_route = "/"
handle_route_change = controller.handle_route_change
