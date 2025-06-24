from textual.app import App, ComposeResult
from textual.widgets import Static
from textual_coloromatic import Coloromatic

my_pattern = """\
-(-)
-)-(\
"""

class MyTextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    Coloromatic { 
        width: 60%; height: 60%; 
        align: center middle;
        border: heavy $panel;
    } 
    .banner {
        width: auto; height: auto; 
        border: tall $accent-darken-2;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:

        with Coloromatic(
            my_pattern,
            repeat=True,
            colors=[
                "#663399",
                "rgb(124,76,205)",
                "steelblue",
                "$accent"
            ],
            animate=True,
            # animation_type="smooth_strobe"
            horizontal=True,
            reverse=True,
            fps=15,
            id="my_coloromatic1"
        ):
            yield Static("Your content here", classes="banner")


MyTextualApp().run()
