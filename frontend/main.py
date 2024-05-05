import flet as ft
from controllers import handle_route_change, initial_route


def main(page: ft.Page):
    page.on_route_change = lambda route: handle_route_change(route, page)
    page.go(initial_route)


if __name__ == "__main__":
    ft.app(target=main)
