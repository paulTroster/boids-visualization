import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from dataclasses import dataclass


@dataclass
class SliderWithLabel:
    slider: Slider
    label: TextBox

    def __init__(
        self,
        screen: pygame.Surface,
        slider_name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        min_value: int,
        max_value: int,
        step: float,
        label_font_size: int = 30,
    ):
        # TextBox to show slider_name
        self.name_label = TextBox(
            screen,
            x + width // 2 - 50,
            y - 40,
            100,
            30,
            fontSize=15,
        )
        self.name_label.setText(slider_name)
        self.slider = Slider(
            screen, x, y, width, height, min=min_value, max=max_value, step=step
        )
        self.label = TextBox(
            screen,
            x + width // 2 - 50,
            y + height + 10,
            100,
            50,
            fontSize=label_font_size,
        )

    def update_label(self):
        self.label.setText(str(self.slider.getValue()))

    def get_value(self) -> float:
        return float(self.slider.getValue())
