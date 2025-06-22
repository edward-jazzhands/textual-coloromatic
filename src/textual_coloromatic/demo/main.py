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
from textual import on  # , log
import textual.events as events
from textual.theme import Theme
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container, ScrollableContainer
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, Button, Select, Switch, TextArea, Input

# Textual library imports
from textual_slidecontainer import SlideContainer

# Local imports
from textual_coloromatic import Coloromatic
from textual_coloromatic.demo.datawidget import ActiveColors
from textual_coloromatic.demo.settingsbar import SettingsWidget
from textual_coloromatic.demo.screens import HelpScreen, CustomStringScreen
import textual_coloromatic.demo.demo_art


class BottomBar(Horizontal):

    def __init__(self, coloromatic: Coloromatic):
        super().__init__()
        self.coloromatic = coloromatic
        self.stored_custom_str: str = ""

        art_pkg_path = Path(next(iter(getattr(textual_coloromatic.demo.demo_art, "__path__"))))
        self.coloromatic.art_loader.add_directory(art_pkg_path)
        self.file_dict: dict[str, list[Path]] = self.coloromatic.art_loader.file_dict
        """String (key) is the directory name. The value is a list of path objects for each .txt file
        in that directory."""

        art_options: list[Path] = self.file_dict["demo_art"]
        # ? The pattern options are built into the ColorOmatic class:
        # Note you can also access them through the file_dict, but this is more convenient.
        pattern_options: dict[str, Path] = self.coloromatic.pattern_options

        self.art_options: list[tuple[str, Path]] = []
        for path in art_options:
            display_name = path.name.replace(path.suffix, "")
            self.art_options.append((display_name, path))

        self.pattern_options: list[tuple[str, Path]] = []
        for key, path in pattern_options.items():
            self.pattern_options.append((key, path))

    def compose(self) -> ComposeResult:

        yield Select(self.art_options, id="art_select", allow_blank=True)
        yield Button("Random", id="randomize_button")
        yield Button("Custom", id="custom_button")
        yield Switch(id="art_pattern_switch")
        yield Static("Toggle showing art or patterns", classes="bottombar_item")

    @on(Button.Pressed, "#randomize_button")
    def randomize_art(self) -> None:

        art_select = cast(Select[Path], self.query_one("#art_select", Select))
        current_selection = art_select.value
        possible_choices: list[Path] = []

        if self.query_one(Switch).value:  #         pattern mode
            for path in self.file_dict["patterns"]:
                if path != current_selection:
                    possible_choices.append(path)
        else:  #                                    art mode
            for path in self.file_dict["demo_art"]:
                if path != current_selection:
                    possible_choices.append(path)

        art_select.value = random.choice(possible_choices)

    @on(Button.Pressed, "#custom_button")
    def custom_str_button(self) -> None:

        self.app.push_screen(CustomStringScreen(self.stored_custom_str), callback=self.update_with_custom)

    def update_with_custom(self, new_str: str | None) -> None:

        if new_str:
            self.log.debug(f"{new_str = }")
            self.stored_custom_str = new_str
            self.coloromatic.text_input = new_str

    @on(Select.Changed, selector="#art_select")
    def art_changed(self, event: Select.Changed) -> None:

        if event.value == Select.BLANK:  # why is blank allowed again?
            return
        assert isinstance(event.value, Path)

        # Each Path object is a .txt file, here we just want the name without the suffix.
        # The pattern options are built into the ColorOmatic class, but I also added
        # in a demo_art directory for the sake of the demo. So this will look up
        # if the current choice is in the built-in patterns.
        choice = event.value.name.replace(event.value.suffix, "")
        if choice in self.coloromatic.pattern_options:
            self.coloromatic.set_pattern(choice)
        else:
            self.coloromatic.update_from_path(event.value)

    @on(Switch.Changed)
    def switch_changed(self, event: Switch.Changed) -> None:

        art_select = cast(Select[Path], self.query_one("#art_select", Select))
        if event.value:  # on = show patterns
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

        # assign coloromatic to variable for passing in to SettingsWidget and BottomBar
        coloromatic = Coloromatic(id="coloromatic")
        main_window = ScrollableContainer(id="main_window")

        # Note: Layout is horizontal. (top of styles.tcss)
        yield Header()
        with SlideContainer(id="menu_container", slide_direction="left", floating=False):
            yield SettingsWidget(coloromatic, main_window)
        with Container():
            with main_window:
                with coloromatic:
                    child_static = TextArea("Sample text. You can edit this text.", id="child_static")
                    child_static.display = False
                    yield child_static
            yield BottomBar(coloromatic)
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.app.theme_changed_signal.subscribe(self, self._refresh_theme)  # type: ignore[unused-ignore]

    async def _refresh_theme(self, theme: Theme) -> None:
        settings_widget = self.query_one(SettingsWidget)
        bg_input = settings_widget.query_one("#bg_coloromatic", Input)
        await bg_input.action_submit()

    @on(Coloromatic.Updated)
    def coloromatic_updated(self, event: Coloromatic.Updated) -> None:

        self.log.debug(f"Coloromatic Updated: {event}")

        settings_widget = self.query_one(SettingsWidget)
        settings_widget.update_size_label(
            f"Current size: {event.widget.size.width}W x {event.widget.size.height}H"
        )

        # See if repeating mode was just set. This would be set automatically by using
        # built in patterns. If so, we need to make sure the tiling switch is set to ON.
        if event.widget.repeat:
            tiling_switch = settings_widget.query_one("#tiling_switch", Switch)
            if not tiling_switch.value:
                tiling_switch.value = True
                # tiling_switch.disabled = True
                # tiling_switch.tooltip = "Tiling is ON when using patterns."

        # If the widget is animating all the colors are removed except for one (or none),
        # it will internally stop the animation. When it does that, we need to update the
        # animate switch in the demo menu to reflect that.
        animate_switch = settings_widget.query_one("#animate_switch", Switch)
        if event.animated:
            animate_switch.value = event.animated

        active_colors = self.query_one(ActiveColors)
        if len(active_colors) <= 1:
            if animate_switch.value is True:  # safety
                animate_switch.value = False
            animate_switch.disabled = True
            animate_switch.tooltip = "Set at least 2 colors to animate."
        else:
            animate_switch.disabled = False
            animate_switch.tooltip = None

    @on(ActiveColors.Updated)
    def activecolors_updated(self, event: ActiveColors.Updated) -> None:

        active_colors = cast(ActiveColors, event.widget)
        self.log.debug(active_colors)
        self.query_one(Coloromatic).set_color_list([item[0] for item in active_colors])

    def action_toggle_menu(self) -> None:
        self.query_one(SlideContainer).toggle()

    def action_show_help(self) -> None:
        self.push_screen(HelpScreen())


def run_demo() -> None:
    """Run the demo app."""
    app = ColoromaticDemo()
    app.run()


if __name__ == "__main__":
    run_demo()
