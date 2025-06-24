# STANDARD LIBRARY IMPORTS
from __future__ import annotations

# Textual imports
from textual.app import App, ComposeResult
from textual.widgets import Static

# Local imports
from textual_coloromatic import Coloromatic

my_pattern = "<->[-]"

class TextualApp(App[None]):


    CSS = """
    Coloromatic { width: 1fr; height: 10; align: center middle; } 
    .banner { width: auto; border: tall $panel; padding: 0 1; }
    """

    def compose(self) -> ComposeResult:

        with Coloromatic(pattern="brick1", colors=["red", "blue"]):
            yield Static("Your content here", classes="banner")

        yield Coloromatic(
            my_pattern,
            colors=["maroon", "#1ed760", "rgb(255, 0, 255)"],
            horizontal=True,
            id="my_coloromatic1",
        )

    def on_mount(self) -> None:

        my_coloromatic = self.query_one("#my_coloromatic1", Coloromatic)
        my_coloromatic.repeat = True


TextualApp().run()
