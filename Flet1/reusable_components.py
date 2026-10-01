import flet as ft
from flet import  Page, Row, TextField, ElevatedButton, MainAxisAlignment

from flet_core.control_event import ControlEvent

# SOMETHING IS WRONG, TO CHECK

class MyButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.bgcolor = ft.Colors.ORANGE_300
        self.color = ft.Colors.GREEN_800
        self.text = text
        self.on_click = on_click

# This does no longer work as it was built on UserControl that was deprecated
class IncrementCounter(ft.Text):

    def __init__(self, text: str, start_number: int=0, ) -> None:
        super().__init__()
        self.text = text
        self.counter = start_number
        self.text_number: TextField = TextField(value = str(self.counter))

    def increment(self, e: ControlEvent) -> None:
        self.counter += 1
        self.text_number.value = str(self.counter)
        self.update()

# SOMETHING WRONG HERE

    def build(self) -> Row:
        return Row(
            controls=[
                MyButton(self.text, on_click=self.increment ),
                self],

            alignment=MainAxisAlignment.SPACE_BETWEEN,
            width=100
        )

def main(page: Page) -> None:
    page.title = "Reusable App"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    page.add(IncrementCounter("People"))
    page.add(IncrementCounter("Cars", 5))
    page.add(IncrementCounter("Trucks", 2))
    page.update()



if __name__ == "__main__":
    ft.app(target=main)