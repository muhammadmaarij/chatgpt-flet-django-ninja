import flet as ft


def create_signup_view(page: ft.Page, username_input: ft.TextField, password_input: ft.TextField, password_confirm_input: ft.TextField, sign_up: callable):
    return ft.View(
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
                            ft.ElevatedButton("Sign Up", on_click=sign_up),
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


def create_login_view(page: ft.Page, username_input: ft.TextField, password_input: ft.TextField, login: callable):
    return ft.View(
        "/login",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Login"),
                        username_input,
                        password_input,
                        ft.Row([
                            ft.ElevatedButton("Login", on_click=login),
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


def create_chat_view(page: ft.Page, chat_input: ft.TextField, chat_output: ft.Column, send_message: callable, new_chat: callable):
    appbar = ft.AppBar(
        leading=ft.Container(
            content=ft.Image(src="https://via.placeholder.com/50"),
            padding=ft.Padding(left=10, top=0, right=10, bottom=0),
        ),
        title=ft.Text("ChatGPT-like Page"),
        center_title=True,
        actions=[
            ft.Container(content=ft.TextButton("Link 1", on_click=lambda e: page.go(
                "/link1")), padding=ft.Padding(left=10, top=0, right=10, bottom=0)),
            ft.Container(content=ft.TextButton("Link 2", on_click=lambda e: page.go(
                "/link2")), padding=ft.Padding(left=10, top=0, right=10, bottom=0)),
        ],
    )

    sidebar_column = ft.Column(controls=[], spacing=5)
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
            [ft.Container(content=chat_output, expand=True), bottom_bar],
            expand=True,
        ),
        expand=True,
        padding=10,
        bgcolor=ft.colors.WHITE,
    )

    return ft.View(
        "/chat",
        [
            appbar,
            ft.Row(
                [sidebar, content],
                expand=True,
            ),
        ]
    )


def create_home_view(page: ft.Page):
    return ft.View(
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
