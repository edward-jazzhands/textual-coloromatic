"settingsbar.py - Settings bar for the Coloromatic demo app.\n"

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

from __future__ import annotations

# Textual imports
from textual import on  # , log
from textual.app import ComposeResult
from textual.containers import Horizontal, Container, VerticalScroll
from textual.widget import Widget
from textual.widgets import Static, Input, Select, Switch, Button, TextArea

# Local imports
from textual_coloromatic import Coloromatic
from textual_coloromatic.demo.validators import (
    QualityValidator,
    FPSValidator,
    SizeValidator,
    ColorValidator,
)
from textual_coloromatic.demo.screens import ColorScreen


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

    def __init__(self, coloromatic: Coloromatic, main_window: Widget):
        super().__init__()
        self.coloromatic = coloromatic
        self.main_window = main_window

    def compose(self) -> ComposeResult:

        tiling = Switch(id="tiling_switch")
        self.width_input = Input(id="width_input", validators=[SizeValidator()], max_length=5)
        self.height_input = Input(id="height_input", validators=[SizeValidator()], max_length=5)
        color_popup_button = Button("Enter Colors", id="color_list_button")
        animation_select = Select(self.animations, value="gradient", id="animation_select", allow_blank=False)
        animate_switch = Switch(False, id="animate_switch", disabled=True)
        horizontal_switch = Switch(id="horizontal_switch")
        reverse_switch = Switch(id="reverse_switch")
        gradient_quality = Input(
            id="gradient_quality",
            max_length=3,
            validators=[QualityValidator()],
        )
        animation_fps = Input(
            id="animation_fps",
            max_length=4,
            validators=[FPSValidator()],
        )
        child_switch = Switch(False, id="show_child")
        border_switch = Switch(id="border_switch", value=False)
        bg_coloromatic = Input(id="bg_coloromatic", validators=[ColorValidator(self.app.theme_variables)])

        yield Static("Settings", id="settings_title")
        yield Static("*=details in help (F1)", id="help_label")
        yield SettingBox(tiling, "Tiling*", widget_width=10)
        yield SettingBox(self.width_input, "Width*", widget_width=12)
        yield SettingBox(self.height_input, "Height*", widget_width=12)
        yield Static("Current size: 0", id="size_label")
        yield SettingBox(color_popup_button, "*")
        yield SettingBox(animation_select, "Animation Type*", widget_width=22, label_position="under")
        yield SettingBox(animate_switch, "Animate", widget_width=10)
        yield SettingBox(horizontal_switch, "Horizontal", widget_width=10)
        yield SettingBox(reverse_switch, "Reverse\nanimation", widget_width=10)
        yield SettingBox(gradient_quality, "Gradient\nquality*", widget_width=12)
        yield SettingBox(animation_fps, "Animation\nFPS*", widget_width=12)
        yield SettingBox(child_switch, "Show child\nwidget*", widget_width=10)
        yield SettingBox(border_switch, "Border", widget_width=10)
        yield SettingBox(bg_coloromatic, "ColorOmatic bg color", widget_width=22, label_position="under")

    @on(Switch.Changed, selector="#tiling_switch")
    async def tiling_switch_toggled(self, event: Switch.Changed) -> None:

        self.coloromatic.repeat = event.value
        if self.width_input.value == "":
            self.width_input.value = "1fr"
            await self.width_input.action_submit()
        if self.height_input.value == "":
            self.height_input.value = "1fr"
            await self.height_input.action_submit()

    @on(Input.Submitted, selector="#width_input")
    def width_input_set(self, event: Input.Submitted) -> None:

        if event.validation_result:
            if event.validation_result.is_valid:
                width = self.width_input.value if self.width_input.value != "" else "auto"
                height = self.height_input.value if self.height_input.value != "" else "auto"
                self.log(f"Setting container size to: ({width} x {height})")

                if width == "auto":
                    self.coloromatic.styles.width = width
                    self.log(f"Width set to: {self.coloromatic.styles.width}")
                else:
                    try:
                        self.coloromatic.styles.width = int(width)
                        self.log(f"Width set to integer: {self.coloromatic.styles.width}")
                    except ValueError:
                        self.coloromatic.styles.width = width
                        self.log(f"Width set to: {self.coloromatic.styles.width}")
                self.coloromatic.post_message(Coloromatic.Updated(self.coloromatic))
            else:
                failures = event.validation_result.failure_descriptions
                self.log(f"Invalid width: {failures}")
                self.notify(f"Invalid width: {failures}", markup=False)

    @on(Input.Submitted, selector="#height_input")
    def height_input_set(self, event: Input.Submitted) -> None:

        if event.validation_result:
            if event.validation_result.is_valid:
                width = self.width_input.value if self.width_input.value != "" else "auto"
                height = self.height_input.value if self.height_input.value != "" else "auto"
                self.log(f"Setting container size to: ({width} x {height})")

                if height == "auto":
                    self.coloromatic.styles.height = height
                    self.log(f"Height set to: {self.coloromatic.styles.height}")
                else:
                    try:
                        self.coloromatic.styles.height = int(height)
                        self.log(f"Height set to integer: {self.coloromatic.styles.height}")
                    except ValueError:
                        self.coloromatic.styles.height = height
                        self.log(f"Height set to: {self.coloromatic.styles.height}")
                self.coloromatic.post_message(Coloromatic.Updated(self.coloromatic))
            else:
                failures = event.validation_result.failure_descriptions
                self.log(f"Invalid height: {failures}")
                self.notify(f"Invalid height: {failures}", markup=False)

    def update_size_label(self, size: str) -> None:
        self.query_one("#size_label", Static).update(size)

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
        """This must be a number between 1-100, or empty for auto.
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
        """This must be a number greater than 0 and maximum of 100."""

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

    @on(Switch.Changed, selector="#show_child")
    def show_child_toggled(self, event: Switch.Changed) -> None:

        child = self.coloromatic.query_one(TextArea)
        child.display = event.value

    @on(Switch.Changed, selector="#border_switch")
    def border_switch_toggled(self, event: Switch.Changed) -> None:

        if event.value:
            self.coloromatic.add_class("bordered")
        else:
            self.coloromatic.remove_class("bordered")

    @on(Input.Submitted, selector="#bg_coloromatic")
    def bg_coloromatic_set(self, event: Input.Submitted) -> None:

        if event.validation_result:
            if event.validation_result.is_valid:
                self.log(f"Coloromatic background set to: {event.value if event.value else "auto"}")
                if event.value == "":
                    self.coloromatic.styles.background = None
                else:
                    if event.value.startswith("$"):
                        self.coloromatic.styles.background = self.app.theme_variables[event.value[1:]]
                    else:
                        self.coloromatic.styles.background = event.value
            else:
                failures = event.validation_result.failure_descriptions
                self.log(f"Invalid color input: {failures}")
                self.notify(f"Invalid color input: {failures}", markup=False)
