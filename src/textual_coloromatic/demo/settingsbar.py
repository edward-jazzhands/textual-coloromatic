"settingsbar.py - Settings bar for the Coloromatic demo app.\n"

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

from __future__ import annotations

# import random
# from pathlib import Path

# Textual imports
from textual import on  # , log
from textual.app import ComposeResult
from textual.containers import Horizontal, Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import (
    Static,
    Input,
    Select,
    Switch,
    Button,
)

# Textual library imports
# from textual_slidecontainer import SlideContainer


# Local imports
# from textual_coloromatic.datawidget import ListDataWidget
from textual_coloromatic import Coloromatic
from textual_coloromatic.demo.validators import QualityValidator, FPSValidator
from textual_coloromatic.demo.screens import ColorScreen

# from textual_coloromatic.art_loader import ArtLoader


class SettingBox(Container):

    def __init__(
        self,
        widget: Widget,
        label: str = "",
        label_position: str = "beside",
        widget_width: int | None = None,
    ):
        """A setting box with a label and a widget. \n
        Static position can be either 'beside' or 'under'"""

        super().__init__()
        self.widget = widget
        self.label = label
        self.label_position = label_position
        self.widget_width = widget_width

    def compose(self) -> ComposeResult:

        if self.widget_width:
            self.widget.styles.width = self.widget_width

        if self.label_position == "beside":
            with Horizontal():
                yield Static(classes="setting_filler")
                if self.label:
                    yield Static(self.label, classes="setting_label")
                yield self.widget
        elif self.label_position == "under":
            with Horizontal():
                yield Static(classes="setting_filler")
                yield self.widget
            with Horizontal(classes="under_label"):
                yield Static(classes="setting_filler")
                if self.label:
                    yield Static(self.label, classes="setting_label")
            self.add_class("setting_under")


class SettingsWidget(VerticalScroll):

    justifications = [
        ("Left", "left"),
        ("Center", "center"),
        ("Right", "right"),
    ]

    animations = [
        ("gradient", "gradient"),
        ("smooth_strobe", "smooth_strobe"),
        ("fast_strobe", "fast_strobe"),
    ]

    patterns = [
        r"^[1-9][0-9]{0,2}$",  # Number between 1-999
        r"^(100|[1-9]?[0-9])%$",  # Percentage
        r"^\d*\.?\d+fr$",  # Float followed by 'fr'
    ]

    def __init__(self, coloromatic: Coloromatic):
        super().__init__()
        self.coloromatic = coloromatic

    def compose(self) -> ComposeResult:

        self.color_popup_button = Button("Enter Colors", id="color_list_button")
        self.animation_select = Select(
            self.animations, value="gradient", id="animation_select", allow_blank=False
        )
        self.animate_switch = Switch(id="animate_switch", value=False)
        self.horizontal_switch = Switch(id="horizontal_switch", value=False)
        self.reverse_switch = Switch(id="reverse_switch", value=False)
        self.gradient_quality = Input(
            id="gradient_quality",
            max_length=3,
            validators=[QualityValidator()],
        )
        self.animation_fps = Input(
            id="animation_fps",
            max_length=4,
            validators=[FPSValidator()],
        )

        yield Static("Settings", id="settings_title")
        yield Static("*=details in help (F1)", id="help_label")
        yield SettingBox(self.color_popup_button, "*")
        yield SettingBox(self.animation_select, "Animation Type*", widget_width=22, label_position="under")
        yield SettingBox(self.animate_switch, "Animate", widget_width=10)
        yield SettingBox(self.horizontal_switch, "Horizontal", widget_width=10)
        yield SettingBox(self.reverse_switch, "Reverse\nanimation", widget_width=10)
        yield SettingBox(self.gradient_quality, "Gradient\nquality*", widget_width=12)
        yield SettingBox(self.animation_fps, "Animation\nFPS*", widget_width=12)

    @on(Button.Pressed, "#color_list_button")
    async def color_list_button_pressed(self) -> None:

        await self.app.push_screen(ColorScreen())

    @on(Switch.Changed, selector="#animate_switch")
    def animate_switch_toggled(self, event: Switch.Changed) -> None:

        self.coloromatic.animated = event.value

    @on(Select.Changed, selector="#animation_select")
    def animation_selected(self, event: Select.Changed) -> None:

        self.coloromatic.set_animation_type(str(event.value))

    @on(Switch.Changed, selector="#horizontal_switch")
    def horizontal_switch_toggled(self, event: Switch.Changed) -> None:

        self.coloromatic.horizontal = event.value

    @on(Switch.Changed, selector="#reverse_switch")
    def reverse_switch_toggled(self, event: Switch.Changed) -> None:

        self.coloromatic.reverse = event.value

    @on(Input.Submitted, selector="#gradient_quality")
    def gradient_quality_set(self, event: Input.Submitted) -> None:
        """Set the gradient quality. (Number of colors in the gradient)\n
        This must be a number between 1-100, or empty for auto.
        Auto mode will set the quality to the height of the widget."""

        if event.validation_result:
            if event.validation_result.is_valid:
                self.log(f"Gradient quality set to: {event.value if event.value else "auto"}")
                if event.value == "":
                    self.coloromatic.gradient_quality = "auto"
                else:
                    self.coloromatic.gradient_quality = int(event.value)
            else:
                failures = event.validation_result.failure_descriptions
                self.log(f"Invalid Gradient quality input: {failures}")
                self.notify(f"Invalid Gradient quality input: {failures}", markup=False)

    @on(Input.Submitted, selector="#animation_fps")
    def animation_fps_set(self, event: Input.Submitted) -> None:
        """Set the animation frames per second. \n
        This must be a number greater than 0 and maximum of 100."""

        if event.validation_result:
            if event.validation_result.is_valid:
                self.log(f"Animation speed set to: {event.value}")
                if event.value == "":
                    self.coloromatic.animation_fps = "auto"
                else:
                    self.coloromatic.animation_fps = float(event.value)
            else:
                failures = event.validation_result.failure_descriptions
                self.log(f"Invalid animation speed input: {failures}")
                self.notify(f"Invalid animation speed input: {failures}", markup=False)
