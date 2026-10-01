import flet as ft
from flet import Page, Row, Text, KeyboardEvent

def main(page: Page) -> None:
    page.title = "Keyboard PRO"
    page.spacing = 30
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    #Create the text views
    key: Text = Text("Key", size=30)
    shift: Text = Text("Shift", size=30, color="red")
    control: Text = Text("Control", size=30, color="blue")
    alt: Text = Text("Alt", size=30, color="green")
    meta: Text = Text("Meta", size=30, color="yellow")

    # Handling keyboard events
    def on_keyboard(e: KeyboardEvent) -> None:
        key.value = e.key
        shift.visible = e.shift
        control.visible =e.ctrl
        alt.visible = e.alt
        meta.visible = e.meta
        print(e.data)
        page.update()

    # Linking the keyboard events to the page
    page.on_keyboard_event = on_keyboard

    # create the page
    page.add(
        Text("Press any combination of keys..."),
        Row(controls=[key, shift, control, alt, meta], alignment=ft.MainAxisAlignment.CENTER)

    )

if __name__ == "__main__":
    ft.app(target=main)