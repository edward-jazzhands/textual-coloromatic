"""Contains the demo app.
This module contains the demo application for Textual-Coloromatic.

It has its own entry script. Run with `textual-coloromatic`.
"""

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

# Python imports
from __future__ import annotations
from typing import Any, cast
from pathlib import Path
import random

# Textual imports
from textual import on #, log
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container, ScrollableContainer
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Button, Select, Switch

# Textual library imports
from textual_slidecontainer import SlideContainer

# Local imports
from textual_coloromatic import Coloromatic
from textual_coloromatic.demo.datawidget import ActiveColors
from textual_coloromatic.demo.settingsbar import SettingsWidget
from textual_coloromatic.demo.screens import HelpScreen, CustomStringScreen
# from textual_coloromatic.art_loader import ArtLoader





class BottomBar(Horizontal):

    def __init__(self, coloromatic: Coloromatic):
        super().__init__()
        self.coloromatic = coloromatic
        self.file_dict: dict[str, list[Path]] = coloromatic.art_loader.load_file_dict()

        self.art_options: list[tuple[str, Path]] = []
        self.pattern_options: list[tuple[str, Path]] = []

        for key, path_list in self.file_dict.items():
            for path in path_list:
                display_name = path.name.replace(path.suffix, "")
                if key == "art":
                    self.art_options.append((display_name, path))  
                elif key == "patterns":
                    self.pattern_options.append((display_name, path))  

    def compose(self) -> ComposeResult:

        yield Select(self.art_options, id="art_select", allow_blank=True)
        yield Button("Random", id="randomize_button")
        yield Button("Custom", id="custom_button")
        yield Switch(id="art_pattern_switch")
        yield Static("Toggle showing art or patterns", classes="bottombar_item")

    @on(Button.Pressed, "#randomize_button")
    def randomize_art(self) -> None:

        art_select = cast(Select[Path], self.query_one("#art_select", Select))
        if self.query_one(Switch).value:    # pattern mode
            art_select.value = random.choice(self.file_dict["patterns"])
        else: # art mode
            art_select.value = random.choice(self.file_dict["art"])    

    @on(Button.Pressed, "#custom_button")
    def custom_str_button(self) -> None:   

        self.app.push_screen(CustomStringScreen(), callback=self.update_with_custom)

    def update_with_custom(self, new_str: str | None):

        if new_str:
            self.coloromatic.text_input = new_str

    @on(Select.Changed, selector="#art_select")
    def art_changed(self, event: Select.Changed) -> None:

        if event.value == Select.BLANK:  # Explain why blank is even allowed.
            return

        self.log(f"Setting art to: {event.value}...")

        if isinstance(event.value, Path):
            self.coloromatic.update_from_path(event.value)

    @on(Switch.Changed)
    def switch_changed(self, event: Switch.Changed):
        
        art_select = cast(Select[Path], self.query_one("#art_select", Select))
        if event.value:     # on = show patterns
             art_select.set_options(self.pattern_options)
        else:
             art_select.set_options(self.art_options)


class ColoromaticDemo(App[Any]):

    BINDINGS = [
        Binding("ctrl+b", "toggle_menu", "Expand/collapse the menu"),
        Binding("f1", "show_help", "Show help"),
    ]

    CSS_PATH = "styles.tcss"
    TITLE = "Textual-Color-O-Matic Demo"

    def compose(self) -> ComposeResult:

        yield ActiveColors()  # fancy data widget for the demo. Not part of the library.

        self.coloromatic = Coloromatic(id="coloromatic")  # * <- This is the widget.

        self.settings_widget = SettingsWidget(self.coloromatic)
        self.bottom_bar = BottomBar(self.coloromatic)
        self.size_display_bar = Static(id="size_display", expand=True)
        self.menu_container = SlideContainer(id="menu_container", slide_direction="left", floating=False)

        # Note: Layout is horizontal. (top of styles.tcss)
        yield Header()
        with self.menu_container:
            yield self.settings_widget
        with Container():
            with ScrollableContainer(id="main_window"):
                yield self.coloromatic
            yield self.size_display_bar
            yield self.bottom_bar
        yield Footer()

    @on(Coloromatic.Updated)
    def coloromatic_updated(self, event: Coloromatic.Updated) -> None:

        # If the widget is animating all the colors are removed except for one (or none),
        # it will internally stop the animation. When it does that, we need to update the
        # animate switch in the demo menu to reflect that.
        if event.animated:
            self.settings_widget.animate_switch.value = event.animated

        active_colors = self.query_one(ActiveColors)
        if len(active_colors) <= 1:
            self.settings_widget.animate_switch.disabled = True
            self.settings_widget.animate_switch.tooltip = "Set at least 2 colors to animate."
        else:
            self.settings_widget.animate_switch.disabled = False
            self.settings_widget.animate_switch.tooltip = None

    @on(ActiveColors.Updated)
    def activecolors_updated(self, event: ActiveColors.Updated) -> None:

        active_colors = cast(ActiveColors, event.widget)
        self.log(active_colors)
        color_name_strings: list[str] = []
        for item in active_colors:
            color_name_strings.append(item[0])

        self.coloromatic.set_color_list(color_name_strings)

    # @on(SlideContainer.SlideCompleted, "#menu_container")
    # def slide_completed(self) -> None:
    #     self.on_resize()

    def action_toggle_menu(self) -> None:
        self.menu_container.toggle()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())


def run_demo() -> None:
    """Run the demo app."""
    app = ColoromaticDemo()
    app.run()


if __name__ == "__main__":
    run_demo()
