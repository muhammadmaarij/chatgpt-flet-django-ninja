import flet as ft
import requests


def main(page: ft.Page):
    base_url = "http://localhost:8000/api/"
    user_token = None
    username = None
    chats = []
    selected_chat_index = 0
    sidebar_column = None  # Global variable to hold the sidebar Column reference

    def update_sidebar():
        sidebar_column.controls.clear()
        for index, chat in enumerate(chats):
            sidebar_column.controls.append(
                ft.TextButton(
                    text=chat["name"],
                    on_click=lambda e, index=index: select_chat(index),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5))
                )
            )
        sidebar_column.controls.append(
            ft.ElevatedButton("New Chat", on_click=new_chat)
        )
        sidebar_column.update()

    def select_chat(index):
        nonlocal selected_chat_index
        selected_chat_index = index
        chat_output.controls.clear()
        chat_output.controls.extend(chats[selected_chat_index]["messages"])
        chat_output.auto_scroll = True
        page.update()

    def new_chat(e):
        chat_name = f"Chat {len(chats) + 1}"
        chats.append({"name": chat_name, "messages": []})
        update_sidebar()
        select_chat(len(chats) - 1)

    def sign_up(e):
        nonlocal username
        username = username_input.value
        password1 = password_input.value
        password2 = password_confirm_input.value
        response = requests.post(
            base_url + "signup", json={"username": username, "password1": password1, "password2": password2})
        result = response.json()
        if result.get("success"):
            page.session.set("user_token", response.cookies.get("sessionid"))
            page.snack_bar = ft.SnackBar(
                ft.Text("Sign up successful!"), open=True)
            page.go("/chat")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {result.get('errors')}"), open=True)
            page.update()

    def login(e):
        nonlocal username
        username = username_input.value
        password = password_input.value
        response = requests.post(
            base_url + "login", json={"username": username, "password": password})
        result = response.json()
        if result.get("success"):
            page.session.set("user_token", response.cookies.get("sessionid"))
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
        user_message_text = ft.Text(f"{username}: {user_message}")
        chats[selected_chat_index]["messages"].append(user_message_text)
        chat_output.controls.append(user_message_text)
        chat_output.controls.append(ft.Divider())
        chat_output.auto_scroll = True
        page.update()

        try:
            response = requests.post(
                base_url + "chat", json={"message": user_message}, cookies={"sessionid": user_token})
            result = response.json()
            bot_message_text = ft.Text(f"ChatGPT: {result.get('response')}")
            chats[selected_chat_index]["messages"].append(bot_message_text)
            chat_output.controls.append(bot_message_text)
            chat_output.controls.append(ft.Divider())
        except requests.exceptions.JSONDecodeError as err:
            error_text = ft.Text("Error: Unable to decode server response.")
            chats[selected_chat_index]["messages"].append(error_text)
            chat_output.controls.append(error_text)
            chat_output.controls.append(ft.Divider())
        except Exception as e:
            error_text = ft.Text(f"An error occurred: {str(e)}")
            chats[selected_chat_index]["messages"].append(error_text)
            chat_output.controls.append(error_text)
            chat_output.controls.append(ft.Divider())
        chat_output.auto_scroll = True
        page.update()

    # Inputs
    username_input = ft.TextField(label="Username", width=300, autofocus=True)
    password_input = ft.TextField(label="Password", password=True, width=300)
    password_confirm_input = ft.TextField(
        label="Confirm Password", password=True, width=300)
    chat_input = ft.TextField(label="Message", expand=True)
    chat_output = ft.Column(auto_scroll=True, expand=True)
    sidebar_controls = []

    # Route change function
    def route_change(route):
        nonlocal sidebar_column
        route_str = route.route
        page.views.clear()
        if route_str == "/signup":
            page.views.append(
                ft.View(
                    "/signup",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Signup"),
                                    username_input,
                                    password_input,
                                    password_confirm_input,
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Sign Up", on_click=sign_up),
                                        ft.ElevatedButton(
                                            "Login Instead", on_click=lambda e: page.go("/login")),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ]
                )
            )
        elif route_str == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Login"),
                                    username_input,
                                    password_input,
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "Login", on_click=login),
                                        ft.ElevatedButton(
                                            "Sign Up Instead", on_click=lambda e: page.go("/signup")),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ]
                )
            )
        elif route_str == "/chat":
            appbar = ft.AppBar(
                leading=ft.Container(
                    content=ft.Image(src="https://via.placeholder.com/50"),
                    padding=ft.Padding(left=15, top=0, right=10, bottom=0),
                ),
                title=ft.Text("ChatGPT-like Page"),
                center_title=True,
                actions=[
                    ft.Container(content=ft.TextButton("Link 1", on_click=lambda e: page.go("/link1")),
                                 padding=ft.Padding(left=10, top=0, right=10, bottom=0)),
                    ft.Container(content=ft.TextButton("Link 2", on_click=lambda e: page.go("/link2")),
                                 padding=ft.Padding(left=10, top=0, right=20, bottom=0)),
                ],
            )

            sidebar_column = ft.Column(controls=sidebar_controls, spacing=5)
            sidebar = ft.Container(
                content=sidebar_column,
                width=200,
                padding=10,
                bgcolor=ft.colors.BLUE_GREY_50,
            )

            bottom_bar = ft.Container(
                content=ft.Row(
                    [
                        chat_input,
                        ft.ElevatedButton("Send", on_click=send_message),
                    ],
                    spacing=5,
                ),
                padding=10,
                bgcolor=ft.colors.LIGHT_BLUE_50,
            )

            chat_content = ft.Column(
                [
                    chat_output,
                    bottom_bar,
                ],
                expand=True,
            )

            content = ft.Container(
                content=ft.Column(
                    [ft.Container(content=chat_output,
                                  expand=True), bottom_bar],
                    expand=True,
                ),
                expand=True,
                padding=10,
                bgcolor=ft.colors.WHITE,
            )

            page.views.append(
                ft.View(
                    "/chat",
                    [
                        appbar,
                        ft.Row(
                            [sidebar, content],
                            expand=True,
                        ),
                    ],
                )
            )
            page.update()
            new_chat(None)  # Initialize with a new chat
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("Welcome!"),
                        ft.Row([
                            ft.ElevatedButton(
                                "Sign Up", on_click=lambda e: page.go("/signup")),
                            ft.ElevatedButton(
                                "Login", on_click=lambda e: page.go("/login")),
                        ]),
                    ]
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)
