import flet as ft
from flet import  Text

def main(page: ft.Page) -> None:
    page.title = "Hot Reload"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    text: Text = Text(value= "This is some text",
                      text_align=ft.TextAlign.CENTER,
                      width=200,
                      size=30,
                      color='green')

    page.add(text)


if __name__ == "__main__":
    ft.app(target=main)


# Core message: run it from the command line with flet run hot_reload.py
# to make it hot-reloadable (changes will show upon saving the file)