# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING
import random
if TYPE_CHECKING:
    pass

# Textual imports
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Placeholder, Static
from textual.containers import Horizontal

# Local imports
from textual_coloromatic import Coloromatic

#############
# constants #
#############
color_list = ["blue", "magenta", "yellow"]
gradient_quality = 10
fps_sides = 6
fps_tops = 15
symbol_top = "▄"
symbol_bottom = "▀"
symbol_side = "█"
#############

class TextualApp(App[None]):

    CSS = """
    Screen { align: center middle; }  
    .my_container {
        align: center middle;
        width: 50; height: 10;
    }
    .top_bottom { width: 1fr; height: 1; }
    .left_right { width: 1;   height: 1fr; }
    #pattern    { 
        align: center middle;    
        width: 50; height: 10;
        margin: 5 0;
        # border: solid $primary; 
        & > Static { width: auto; }
    }
    Placeholder { width: 1fr; height: 1fr; }      
    """

    BINDINGS = [("r", "reverse", "Reverse Animation")]

    def compose(self) -> ComposeResult:

        with Container(classes="my_container"):
            yield Coloromatic(
                symbol_top,
                repeat=True,
                gradient_quality=gradient_quality*2,
                colors=color_list,
                animate=True,
                horizontal=True,
                fps=fps_tops,
                classes="top_bottom"
            )
            with Horizontal(id="middle_row"):
                yield Coloromatic(
                    symbol_side,
                    repeat=True,
                    gradient_quality=gradient_quality,
                    colors=color_list,
                    animate=True,
                    reverse=True,
                    fps=fps_sides,
                    classes="left_right",
                )
                yield Placeholder()
                yield Coloromatic(
                    symbol_side,
                    repeat=True,
                    gradient_quality=gradient_quality,
                    colors=color_list,
                    animate=True,
                    fps=fps_sides,
                    classes="left_right",
                )
            yield Coloromatic(
                symbol_bottom,
                repeat=True,
                gradient_quality=gradient_quality*2,
                colors=color_list,
                animate=True,
                horizontal=True,
                reverse=True,
                fps=fps_tops,
                classes="top_bottom",
                id="bottom_row"               
            )  
        with Coloromatic(
            # repeat=True,
            pattern="brick2",
            colors=color_list,
            animate=True,
            id="pattern"               
        ):
            yield Static("Hello", id="pattern_text")             

        yield Footer()

    def on_mount(self):
        self.set_interval(5, self.update_text)

    def update_text(self):

        phrases = [
            "Hello, \nWorld",
            "Good stuff, \nI do say",
            "My milkshake brings \nall the boys to the yard",
            "I come from a land \ndown under",
            "Whoa, we're half way there \nTake my hand, we'll make it, I swear",
            "Never gonna give you up, \nnever gonna let you down",
        ]
        static = self.query_one("#pattern_text", Static)
        static.update(random.choice(phrases))

    def action_reverse(self):
        coloromatics = self.query(Coloromatic).results()
        for coloromatic in coloromatics:
            coloromatic.reverse = not coloromatic.reverse


TextualApp().run()
