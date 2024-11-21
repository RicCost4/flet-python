import flet as ft
from typing import Any
from utils.constants import Constants

class Flet_tags:
    constants = Constants()
    @classmethod
    def button(cls, title:str, function:Any | None, color:str, bg_color:str = constants.color_purple) -> ft.ElevatedButton:
        return ft.ElevatedButton(text=title, on_click=function, bgcolor=bg_color, color=color)

    @classmethod
    def inputs(cls, text_label:str) -> ft.TextField:
        return ft.TextField(label=text_label)

    @classmethod
    def text(cls, value:str, color:str, size:int = 12, weight:str = None) -> ft.Text:
        return ft.Text(value=value,size=size, color=color, weight=weight)
