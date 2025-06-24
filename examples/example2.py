from textual.app import App, ComposeResult
from textual.widgets import Footer
from textual_coloromatic import Coloromatic

banner = r"""
          ▀█▀ █▀▀ ▀▄▀ ▀█▀ █░█ ▄▀█ █░░  ▄▄          
          ░█░ ██▄ █░█ ░█░ █▄█ █▀█ █▄▄  ░░          
                                                   
█▀▀ █▀█ █░░ █▀█ █▀█ ▄▄ █▀█ ▄▄ █▄░▄█ ▄▀█ ▀█▀ ▀█▀ █▀▀
█▄▄ █▄█ █▄▄ █▄█ █▀▄ ░░ █▄█ ░░ █░▀░█ █▀█ ░█░ ▄█▄ █▄▄
"""


class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }
    Coloromatic { width: 1fr; height: 16; align: center middle; } 
    .banner {
        width: auto; height: auto; 
        border: tall $accent-darken-2;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:

        with Coloromatic(
            banner,
            pattern="weave",
            colors=["black", "white"],
            animate=True,
            horizontal=True,
            fps=30,
        ):
            yield Coloromatic(
                banner,
                colors=["$primary", "$accent"],
                animate=True,
                fps=5,
                classes="banner"
            )
        yield Footer()


TextualApp().run()
