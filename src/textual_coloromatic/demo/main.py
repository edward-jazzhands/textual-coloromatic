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
from textual import on, log
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container, ScrollableContainer
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Button, Select

# Textual library imports
from textual_slidecontainer import SlideContainer

# Local imports
from textual_coloromatic import Coloromatic
from textual_coloromatic.demo.datawidget import ActiveColors
from textual_coloromatic.demo.settingsbar import SettingsWidget
from textual_coloromatic.demo.screens import HelpScreen
from textual_coloromatic.art_loader import ArtLoader


class BottomBar(Horizontal):

    def __init__(self, coloromatic: Coloromatic):
        super().__init__()
        self.coloromatic = coloromatic
        self.art_loader = ArtLoader()
        self.art_list: list[Path] = self.art_loader.load_art_file_list()

        self.art_selections: list[tuple[str, Path]] = []
        for path in self.art_list:
            log(f"Loaded path: {path.name}")
            display_name = path.name.replace(path.suffix, "")
            self.art_selections.append((display_name, path))

    def compose(self) -> ComposeResult:

        yield Select(self.art_selections, id="art_select", allow_blank=True)
        yield Button("Random Art", id="randomize_button")

    @on(Button.Pressed, "#randomize_button")
    def randomize_art(self) -> None:

        art_select = cast(Select[Path], self.query_one("#art_select", Select))
        art_select.value = random.choice(self.art_list)  # triggers method art_changed (below)

    @on(Select.Changed, selector="#art_select")
    def art_changed(self, event: Select.Changed) -> None:

        if event.value == Select.BLANK:  # Explain why blank is even allowed.
            return

        self.log(f"Setting art to: {event.value}...")

        if isinstance(event.value, Path):
            self.coloromatic.update_from_path(event.value)


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
    def activecolors_updated(self) -> None:

        active_colors = self.query_one(ActiveColors)
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
