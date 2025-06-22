"""Module for the Coloromatic class."""

# ~ Type Checking (Pyright and MyPy) - Strict Mode
# ~ Linting - Ruff
# ~ Formatting - Black - max 110 characters / line

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING, get_args
from pathlib import Path

if TYPE_CHECKING:
    # from textual.visual import VisualType
    from textual import events
    from textual.geometry import Size  # , Region

from typing import cast
from typing_extensions import Literal  # , get_args
from collections import deque
from copy import deepcopy

# Textual and Rich imports
from textual import on
from textual.theme import Theme
from textual.color import Gradient, Color

# from textual.css.scalar import Scalar
from textual.message import Message
from textual.strip import Strip
from textual.widget import Widget

# from textual.widgets import Static
# from textual.containers import Container
from textual.reactive import reactive
from textual.timer import Timer
from rich.segment import Segment
from rich.style import Style

# Local imports
from textual_coloromatic.art_loader import ArtLoader
import textual_coloromatic.patterns

# LITERALS:
COLOR_MODE = Literal["color", "gradient", "none"]
ANIMATION_TYPE = Literal["gradient", "smooth_strobe", "fast_strobe"]
PATTERNS = Literal[
    "brick1",
    "brick2",
    "crosses",
    "fence1",
    "fence2",
    "fish",
    "hive",
    "honeycomb1",
    "honeycomb2",
    "honeycomb3",
    "jaggedwave",
    "persian",
    "squares",
    "tesselation1",
    "tesselation2",
    "tesselation3",
    "triangles",
    "weave",
]


class Coloromatic(Widget):

    DEFAULT_CSS = "Coloromatic {width: auto; height: auto;}"

    ############################
    # ~ Public API Reactives ~ #
    ############################

    text_input: reactive[str] = reactive("", always_update=True)
    """The content to render in the Coloromatic. This is a string that can be any text you want.
    It can be a single line or multiple lines."""

    list_input: reactive[list[str] | None] = reactive(None, always_update=True)
    """The content to render in the Coloromatic. This is the same as text_input but it will take
    a list of strings instead of a single string.
    list_input is None by default. If used it will override text_input."""

    repeat: reactive[bool] = reactive(False, always_update=True)
    """Setting this to true will make the content in the Coloromatic repeat to fill the entire
    space of the Coloromatic. This can be used to make tiling effects. It is also set to True
    automatically if a pattern is set."""

    pattern: reactive[PATTERNS | None] = reactive(None, always_update=True)
    """Choose a built-in pattern from the list of available patterns.
    If this is set, there is no need to set the text_input or list_input directly."""

    color_list: reactive[list[str]] = reactive([], always_update=True)
    """A list of colors to use for the gradient. This is a list of strings that can be parsed by a
    Textual Color object. The list can be any number of colors you want. It also supports
    passing in Textual CSS variables ($primary, $secondary, $accent, etc). When using
    CSS variables, they will update automatically to match the theme whenever the user
    of your app changes the theme."""

    animated: reactive[bool] = reactive(False, always_update=True)
    """Whether to animate the gradient. This is a boolean value. If True, the gradient will
    animate."""

    animation_type: reactive[ANIMATION_TYPE] = reactive("gradient", always_update=True)
    """The type of animation to use for the gradient. This is a string literal type that can
    be 'gradient', 'smooth_strobe', or 'fast_strobe'. The default is 'gradient'. 
    - 'gradient' will animate the current gradient it in the direction you specify
    (using the horizontal and reverse settings).
    - 'smooth_strobe' will create a gradient and animate through the colors.
    - 'fast_strobe' will hard switch to the next color in the list.
    It does not make a gradient, and gradient_quality will be ignored."""

    animation_fps: reactive[float | str] = reactive("auto", always_update=True)
    """The Frames per second for the animation. This is a float so that you can set it to values
    such as 0.5 if you desire. The default is 'auto', which will set the FPS to 12 for 'gradient',
    12 for 'smooth_strobe', and 1 for 'fast_strobe'."""

    gradient_quality: reactive[int | str] = reactive("auto", always_update=True)
    """The quality of the gradient. This means how many colors the gradient has
    in it. This is either 'auto' or an integer between 3 and 100. The higher the
    number, the smoother the gradient will be. By default, in auto mode,
    this will be calculated depending on the current animation type.
    - In gradient mode, if vertical, it will be calculated based on the height of the widget.
    If horizontal, it will be calculated based on the width of the widget.
    - In smooth_strobe mode, it will be set to (number of colors * 10).
    - In fast_strobe mode, this setting is ignored."""

    horizontal: reactive[bool] = reactive(False, always_update=True)
    """Whether the gradient should be horizontal or vertical. This is a boolean value. If
    True, the gradient will be horizontal. If False, the gradient will be vertical.
    Note that this will have no effect if the animation mode is 'smooth_strobe' or
    'fast_strobe' because they do not use a direction."""

    reverse: reactive[bool] = reactive(False, always_update=True)
    """Whether the animation should run in reverse. This is a boolean value. If True, the
    animation will run in reverse. If False, the animation will run normally. If horizontal 
    is False, this will switch between up and down. If horizontal is True, this will switch 
    between left and right.  
    Note that this will have no effect if the animation mode is 'smooth_strobe' or 'fast_strobe'
    because they do not use a direction."""

    #########################
    # ! Private Reactives ! #
    #########################
    _animation_lines: reactive[list[str]] = reactive(list, layout=True)
    _color_mode: reactive[COLOR_MODE] = reactive("none", always_update=True)

    class Updated(Message):
        """Message sent when the Coloromatic is updated."""

        def __init__(
            self,
            widget: Coloromatic,
        ) -> None:
            super().__init__()

            self.widget = widget
            "The Coloromatic that was updated."
            self.color_mode = widget._color_mode
            "The color mode that was set. This is a string literal type that can be 'color', 'gradient', or 'none'."
            self.animated = widget.animated
            "Whether the Coloromatic is animated. This is a boolean value."

        @property
        def control(self) -> Coloromatic:
            return self.widget

    def __init__(
        self,
        content: str = "",
        *,
        repeat: bool = False,
        pattern: PATTERNS | None = None,
        colors: list[str] = [],
        animate: bool = False,
        animation_type: ANIMATION_TYPE = "gradient",
        gradient_quality: int | str = "auto",
        horizontal: bool = False,
        reverse: bool = False,
        fps: float | str = "auto",
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        """
        Yar

        Args:
            content: The content to render in the Coloromatic. It can be a single
                line or multiple lines.
            repeat: Setting this to true will make the content in the Coloromatic repeat to fill the
                entire space of the Coloromatic. This can be used to make tiling effects. It is also
                 set to True automatically if a pattern is set.
            pattern: Choose a built-in pattern from the list of available patterns.
                If this is set, there is no need to set the text_input or list_input directly.
            colors: List of colors to use for the gradient. This is a list of strings that can be
                parsed by a Textual `Color` object that allows passing in any number of colors you want.
                It also supports passing in Textual CSS variables ($primary, $secondary, $accent, etc).
                If using CSS variables, they will update automatically to match the theme whenever
                the theme is changed.
            animate: Whether to animate the gradient.
            animation_type: Can be 'gradient', 'smooth_strobe', or 'fast_strobe'. The default is 'gradient'.
                - 'gradient' will animate the current gradient it in the direction you specify
                (using the horizontal and reverse settings).
                - 'smooth_strobe' will create a gradient and animate through the colors.
                - 'fast_strobe' will hard switch to the next color in the list.
                It does not make a gradient, and gradient_quality will be ignored.
            gradient_quality: The quality of the gradient. This means how many colors the gradient has
                in it. This is either 'auto' or an integer between 3 and 100. The higher the
                number, the smoother the gradient will be. By default, in auto mode,
                this will be calculated depending on the current animation type.
                - In gradient mode, if vertical, it will be calculated based on the height of the widget.
                If horizontal, it will be calculated based on the width of the widget.
                - In smooth_strobe mode, it will be set to (number of colors * 10).
                - In fast_strobe mode, this setting is ignored.
            horizontal: Whether the gradient should be horizontal or vertical.
                Note that this will have no effect if the animation mode is 'smooth_strobe' or 'fast_strobe'
                because they do not use a direction.
            reverse: Whether the animation should run in reverse.
                If horizontal is False, this will switch between up and down. If horizontal is True, this
                will switch between left and right.
                Note that this will have no effect if the animation mode is 'smooth_strobe' or 'fast_strobe'
                because they do not use a direction. It also does not have an effect on the order of
                the colors (To change the color order, insert the color list in a different order)
            fps: The Frames per second for the animation.
                This is a float so that you can set it to values such as 0.5 if you desire. The default
                is 'auto', which will set the FPS to 12 for 'gradient', 12 for 'smooth_strobe', and 1
                for 'fast_strobe'.
            name: Name of widget.
            id: ID of Widget.
            classes: Space separated list of class names.
        """
        # NOTE: The Widget has to wait to be fully mounted before
        # it can know its maximum width and set the render size.
        # This is because in modes 'auto', 'percent', and 'fraction', PyFiglet needs to
        # know the maximum width of the widget to render the text properly.

        # When the widget receives its first on_resize event (The first time it learns
        # what its proper size will be), it will set the render size.
        # If in auto mode, the max render size is the width of whatever is the
        # parent of the Widget in the DOM. If not in auto, the max render size is
        # the width of the widget itself. (So for example if the widget is set to 1fr,
        # when it finally receives its first resize event, it will check its actual width
        # in cells and then set the maximum render size to that number.)

        super().__init__(name=name, id=id, classes=classes)

        self._initialized = False

        patterns_pkg_path = Path(next(iter(getattr(textual_coloromatic.patterns, "__path__"))))
        self.art_loader = ArtLoader([patterns_pkg_path])
        file_dict: dict[str, list[Path]] = self.art_loader.file_dict
        patterns_list = file_dict["patterns"]
        self.pattern_options: dict[str, Path] = {}
        for path in patterns_list:
            display_name = path.name.replace(path.suffix, "")
            self.pattern_options[display_name] = path

        self._color_obj_list: list[Color] = []
        self._line_colors: deque[Style] = deque([Style()])
        self._gradient: Gradient | None = None
        self._interval_timer: Timer | None = None
        self._size_mode = "auto"  # This is set to auto or not_auto in the refresh_size() method.
        self._direction_int: int = 1  # 1 = forwards, -1 = reverse
        self._fps = 0.0

        self.text_input = content  # note - set both here and in the _complete_init__ method
        self.repeat = repeat
        self.pattern = pattern
        self.animation_fps = fps
        self.horizontal = horizontal
        self.reverse = reverse
        self.color_list = colors
        self.animation_type = animation_type
        self.gradient_quality = gradient_quality
        self.animated = animate

    def _on_mount(self, event: events.Mount) -> None:
        super()._on_mount(event)
        self.app.theme_changed_signal.subscribe(self, self._refresh_theme)  # type: ignore[unused-ignore]
        self.call_after_refresh(self._complete_init__)

    def _refresh_theme(self, theme: Theme) -> None:
        for color in self.color_list:
            if color.startswith("$"):
                self.color_list = self.color_list  # trigger the color list watcher
                return

    def _complete_init__(self) -> None:

        self._initialized = True
        # self.watch_text_input(self.text_input)
        # self.watch_list_input(self.list_input)
        self.mutate_reactive(Coloromatic._animation_lines)
        self.post_message(self.Updated(self))

    #################
    # ~ Public API ~#
    #################

    def update_from_string(self, text: str) -> None:

        self.text_input = text

    def update_from_path(self, path: Path) -> None:

        extracted_art = self.art_loader.extract_art_at_path(path)
        self.list_input = extracted_art

    def set_pattern(self, pattern: str) -> None:
        """Choose a pattern from a list of built-in options.

        Note that this method takes a string instead of a string literal type. This means
        it can take in variables as input, but it will not provide auto-complete for the available
        patterns. To get auto-complete, set the Coloromatic.pattern reactive variable directly."""

        self.pattern = cast(PATTERNS, pattern)

    def set_color_list(self, colors: list[str]) -> None:
        """A list of colors to use for the gradient. This is a list of strings that can be
        parsed by a Textual Color object. The list can be any number of colors you want. It
        also supports passing in Textual CSS variables ($primary, $secondary, $accent, etc).

        Because the color_list variable is reactive, it is required to use the
        mutate_reactive method to set it. This method will do that for you.
        """

        self.color_list = colors  #         Validator method will validate the colors
        self.mutate_reactive(Coloromatic.color_list)

    def set_animation_type(self, animation_type: str) -> None:
        """Set the animation type of the PyFiglet widget.

        This method, unlike setting the reactive property, allows passing in a string
        instead of a string literal type. This is useful for passing in a variable.

        Args:
            animation_type: The animation type to set. Can be 'gradient', 'smooth_strobe', or 'fast_strobe'.
        """

        self.animation_type = cast(ANIMATION_TYPE, animation_type)

    def toggle_animated(self) -> None:
        """Toggle the animated state of the PyFiglet widget.
        The widget will update with the new animated state automatically."""

        self.animated = not self.animated

    def add_directory(self, directory: Path) -> None:
        """Add a new directory to the art loader. After using this method the
        file_dict will be updated to include the new directory.

        Args:
            directory: The directory to add.
        """
        self.art_loader.add_directory(directory)

    @property
    def file_dict(self) -> dict[str, list[Path]]:
        """Get the file dictionary from the art loader. This is a dictionary with the directory name as
        the key and a list of Path objects as the value. The Path objects point to .txt files in that directory.
        """
        return self.art_loader.file_dict

    #################
    # ~ Validators ~#
    #################

    def validate_pattern(self, pattern: PATTERNS | None) -> PATTERNS | None:

        if pattern is None:
            return None

        if pattern and pattern not in get_args(PATTERNS):
            raise ValueError(
                "The entered pattern does not exist in the list of options. Try "
                "setting Coloromatic.patterns directly to get auto-complete for available patterns."
            )
        if pattern not in self.pattern_options:  #! this should not be necessary... here until Im sure
            raise ValueError(f"Pattern {pattern} not found in the list of options.")

        return pattern

    def validate_color_list(self, colors: list[str] | None) -> list[str] | None:

        assert isinstance(colors, (list, type(None))), "Color list must be a list of strings."

        self._color_obj_list.clear()  # Clear the list before adding new colors
        if colors is not None:
            for color in colors:
                if color.startswith("$"):
                    try:
                        color = self.app.theme_variables[color[1:]]
                    except KeyError:
                        self.log.error(f"Color variable {color} not found in theme variables.")
                        raise KeyError(f"Color variable {color} not found in theme variables.")
                try:
                    parsed_color = Color.parse(color)  # Check if the color is valid
                except Exception as e:
                    self.log.error(f"Error parsing color: {e}")
                    raise e
                else:
                    self._color_obj_list.append(parsed_color)
        return colors

    def validate_gradient_quality(self, quality: int | str) -> int | str:

        assert isinstance(quality, (int, str)), "Gradient quality must be an int or 'auto'."

        if quality == "auto":
            return quality
        elif isinstance(quality, int):
            if 3 <= quality <= 100:
                return quality
            else:
                raise ValueError("Gradient quality must be between 3 and 100.")
        else:
            raise Exception("Invalid gradient quality. Must be 'auto' or an integer between 1 and 100.")

    def validate_animation_fps(self, interval: float | str) -> float | str:

        if isinstance(interval, str):
            if interval == "auto":
                return interval
            else:
                raise ValueError("FPS must be a float or 'auto'.")

        if interval <= 0:
            raise ValueError("FPS must be greater than 0.")
        if interval > 60:
            raise ValueError("FPS must be less than or equal to 100.")

        return interval

    def validate_animation_type(self, animation_type: str) -> str:

        if animation_type in ("gradient", "smooth_strobe", "fast_strobe"):
            return animation_type
        else:
            raise ValueError(
                f"Invalid animation type: {animation_type} \nMust be 'gradient', 'smooth_strobe', or 'fast_strobe'."
            )

    ###############
    # ~ Watchers ~#
    ###############

    def watch_text_input(self, text: str) -> None:

        if text == "":
            self._animation_lines = [""]
            self.mutate_reactive(Coloromatic._animation_lines)
        else:
            self._animation_lines = self.special_list_stripper(text.splitlines())
            self.mutate_reactive(Coloromatic._animation_lines)

        if self._initialized:
            self.post_message(self.Updated(self))

    def watch_list_input(self, list_in: list[str] | None) -> None:

        if list_in is None:
            return
        self._animation_lines = self.special_list_stripper(list_in)
        self.mutate_reactive(Coloromatic._animation_lines)

        if self._initialized:
            self.post_message(self.Updated(self))

    def watch_pattern(self, pattern: PATTERNS | None) -> None:

        self.log(f"watch_pattern called with {pattern = }")
        if pattern is None:
            return
        self.repeat = True
        pattern_path_obj = self.pattern_options[pattern]
        self.update_from_path(pattern_path_obj)

    def watch__color_mode(self, color_mode: COLOR_MODE) -> None:

        if color_mode == "none":
            self._line_colors = deque([Style()])
            self._gradient = None  # reset the gradient if it was set
            if self.animated:
                self.animated = False

        elif color_mode == "color":

            color_obj = self._color_obj_list[0]
            assert isinstance(color_obj, Color), "color_obj must be a valid Color object."

            self._line_colors = deque([Style(color=color_obj.rich_color)])
            self._gradient = None  # reset the gradient if it was set
            if self.animated:
                self.animated = False

        elif color_mode == "gradient":
            assert len(self._color_obj_list) >= 1, "Color list is set, but not enough color objects"

            if self.animation_type == "fast_strobe":
                self._line_colors = deque([Style(color=color.rich_color) for color in self._color_obj_list])
                return

            elif self.animation_type == "gradient":

                if self.gradient_quality == "auto":

                    if self.horizontal:
                        to_add = 1 / (len(self._color_obj_list) - 1)
                        gradient_quality = self.size.width * (1.0 + to_add)

                    else:  # vertical
                        to_add = 1 / (len(self._color_obj_list) - 1)
                        gradient_quality = self.size.height * (1.0 + to_add)
                        # MATH EXAMPLE (Calculating `gradient_quality`)

                        # 2 colors: to_add = 1 / (2-1) = +1.0    = 2.0    | double the length
                        # 3 colors: to_add = 1 / (3-1) = +0.5    = 1.5    | add half the total length
                        # 4 colors: to_add = 1 / (4-1) = +0.3333 = 1.3333 | add a third of total
                        # 5 colors: to_add = 1 / (5-1) = +0.25   = 1.25   | add a quarter of the total
                        # 6 colors: to_add = 1 / (6-1) = +0.2    = 1.2    | add a fifth

                    gradient_quality = int(gradient_quality)

                else:
                    assert isinstance(self.gradient_quality, int)
                    gradient_quality = self.gradient_quality

            elif self.animation_type == "smooth_strobe":
                if self.gradient_quality == "auto":
                    gradient_quality = len(self._color_obj_list) * 10
                else:
                    assert isinstance(self.gradient_quality, int)
                    gradient_quality = self.gradient_quality

            else:
                raise RuntimeError("Invalid animation type. This should not happen.")

            if gradient_quality <= 1:
                gradient_quality = 2  # <- this is the minimum quality for a gradient.

            self._gradient = self.make_gradient(self._color_obj_list, gradient_quality)
            assert self._gradient is not None, "Gradient was not created. This should not happen."

            if len(self._gradient.colors) != 0:
                self._line_colors = deque([Style(color=color.rich_color) for color in self._gradient.colors])

        else:
            raise ValueError(f"Invalid color mode: {color_mode}. Must be 'color', 'gradient', or 'none'.")

        if self._initialized:
            self.post_message(self.Updated(self))

    def watch_color_list(self, colors: list[str]) -> None:

        for color in self._color_obj_list:  # this is made by the validator function
            assert isinstance(color, Color), (
                "Color list is set, but found a non-Color object. " "This should not happen."
            )

        # We just set the mode here and then _color_mode takes over.
        if len(self._color_obj_list) == 0:
            self._color_mode = "none"
        elif len(self._color_obj_list) == 1:
            self._color_mode = "color"
        else:  # If its not 0 or 1, it must be 2 or higher.
            self._color_mode = "gradient"

    def watch_animated(self, animated: bool) -> None:

        if animated:
            self.animation_fps = self.animation_fps
        else:
            self.auto_refresh = None

        if self._initialized:
            self.post_message(self.Updated(self))

    def watch_reverse(self, new_value: bool) -> None:

        self._direction_int = -1 if new_value else 1

    def watch_animation_fps(self, fps: float | str) -> None:

        if self.animated:
            if fps == "auto":
                if self.animation_type == "gradient":
                    self.auto_refresh = 1 / 12.0
                elif self.animation_type == "smooth_strobe":
                    self.auto_refresh = 1 / 8.0
                else:  # fast_strobe
                    self.auto_refresh = 1.0
            else:
                self.auto_refresh = 1 / float(fps)
        # else:                             # <- this check should not be necessary.
        # self.auto_refresh = None

    def watch_animation_type(self, animation_type: str) -> None:

        self._color_mode = self._color_mode  #  trigger the reactive to update the colors.
        self.animation_fps = self.animation_fps  # trigger the reactive to update the fps.

    def watch_horizontal(self) -> None:

        self._color_mode = self._color_mode

    def watch_gradient_quality(self) -> None:

        self._color_mode = self._color_mode

    ######################
    # ~ RENDERING LOGIC ~#
    ######################

    @on(Updated)
    def self_updated(self) -> None:
        self.log.debug("Received update event")
        self.query_children().refresh(layout=True)

    def make_gradient(self, colors: list[Color], quality: int) -> Gradient:

        if quality <= 1:
            raise ValueError("Gradient quality must be 2 or greater.")

        for color in colors:
            assert isinstance(color, Color), "Non-valid color object passed into make_gradient."

        temp_colors = colors.copy()
        temp_colors.append(deepcopy(colors[0]))  # <- this is to make it loop back to the first color.

        stops: list[tuple[float, Color]] = []  #        Example with 2 colors (0, 1, 2):
        for i, color in enumerate(temp_colors):  #           0 / 2 = 0.0     third color added for looping
            stop = (i / (len(temp_colors) - 1), color)  #    1 / 2 = 0.5
            stops.append(stop)  #                            2 / 2 = 1.0

        return Gradient(*stops, quality=quality)

    def on_resize(self) -> None:

        if self.size.width == 0 or self.size.height == 0:  # <- this prevents crashing on boot.
            return

        if self.animation_type == "gradient":  # make it recalculate the gradient when size changes.
            self._color_mode = self._color_mode

    # These two functions below are the secret sauce to making the auto sizing work.
    # They are both hooks, and they are called by the Textual framework
    # to determine the size of the widget.
    def get_content_width(self, container: Size, viewport: Size) -> int:

        if self._animation_lines:
            return len(max(self._animation_lines, key=len))
        else:
            return 0

    def get_content_height(self, container: Size, viewport: Size, width: int) -> int:

        if self._animation_lines:
            return len(self._animation_lines)
        else:
            return 0

    def special_list_stripper(self, list_input: list[str]) -> list[str]:

        while True:
            lines_cleaned: list[str] = []
            for i, line in enumerate(list_input):
                if i == 0 and all(c == " " for c in line):  # if first line and blank
                    pass
                elif i == len(list_input) - 1 and all(c == " " for c in line):  # if last line and blank
                    pass
                else:
                    lines_cleaned.append(line)

            if lines_cleaned == list_input:  # if there's no changes,
                break  #                         loop is done
            else:  #                             If lines_cleaned is different, that means there was
                list_input = lines_cleaned  #  a change. So set list_input to lines_cleaned and restart

        # if the figlet output is blank, return 1 empty string
        return [""] if lines_cleaned == [] else lines_cleaned

    def automatic_refresh(self) -> None:

        self.log("Auto refresh method called")

        if self._gradient and self.animated:
            self._line_colors.rotate(self._direction_int)  # 1 = forwards, -1 = reverse
        super().automatic_refresh()

    def render_line(self, y: int) -> Strip:

        if self.repeat:

            try:
                line_index = y % len(self._animation_lines)
                line = self._animation_lines[line_index]
            except IndexError:
                self.log.error("FigletWidget render_lines went out of bounds")
                return Strip.blank(self.size.width)
            except ZeroDivisionError:
                self.log.error("Divizion by zero")
                return Strip.blank(self.size.width)
            except Exception as e:
                raise Exception("Unexpected error in render_line, please examine the cause") from e

            if not line:
                self.log.debug("Not line, returning blank")
                return Strip.blank(self.size.width)
            repeat_count = (self.size.width // len(line)) + 1  # +1 is just extra filler for end
            segment_chars = line * repeat_count

        else:  # not repeat (default)

            if y >= len(self._animation_lines):  # if the line is out of range, return blank
                return Strip.blank(self.size.width)
            try:
                line = self._animation_lines[y]
            except IndexError:
                self.log.error("FigletWidget render_lines went out of bounds")
                return Strip.blank(self.size.width)

            if not line:
                return Strip.blank(self.size.width)
            segment_chars = line

        if self.animation_type == "gradient":

            if not self.horizontal:  #   vertical is normal mode
                color_index = y % len(self._line_colors)  # rotates through the colors.
                return Strip([Segment(segment_chars, style=self._line_colors[color_index])])
            else:
                return Strip(
                    [
                        Segment(char, style=self._line_colors[i % len(self._line_colors)])
                        for i, char in enumerate(segment_chars)
                    ]
                )
        else:  # smooth_strobe or fast_strobe - both change the whole figlet 1 color at a time.
            return Strip([Segment(segment_chars, style=self._line_colors[0])])
