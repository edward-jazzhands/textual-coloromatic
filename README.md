<!-- GitHub prefers-color-scheme method -->
<picture class="only-github">
  <source media="(prefers-color-scheme: dark)" srcset="https://edward-jazzhands.github.io/assets/textual-coloromatic/banner-dark-theme.gif">
  <img src="https://edward-jazzhands.github.io/assets/textual-coloromatic/banner-light-theme.gif">
</picture>

# Textual-Color-O-Matic

[![badge](https://img.shields.io/badge/linted-Ruff-blue?style=for-the-badge&logo=ruff)](https://astral.sh/ruff)
[![badge](https://img.shields.io/badge/formatted-black-black?style=for-the-badge)](https://github.com/psf/black)
[![badge](https://img.shields.io/badge/type_checked-MyPy_(strict)-blue?style=for-the-badge&logo=python)](https://mypy-lang.org/)
[![badge](https://img.shields.io/badge/Type_checked-Pyright_(strict)-blue?style=for-the-badge&logo=python)](https://microsoft.github.io/pyright/)
[![badge](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](https://opensource.org/license/mit)
[![badge](https://img.shields.io/badge/framework-Textual-blue?style=for-the-badge)](https://textual.textualize.io/)

Textual-Color-O-Matic is a [Textual](https://github.com/Textualize/textual) library for color animations and tiling effects.

It is designed to make it easy to animate strings with cool color effects, as well as set background patterns that can function as wallpaper or backdrops for widgets.

## Features

- Color system built on Textual's color system. Thus, it can display any color in the truecolor/16-bit spectrum,
and can take common formats such as hex code and RGB, or just a huge variety of named colors.
- Make a gradient automatically between any two colors, or through any number of colors.
- Animation system that's simple to use. Just make your gradient and toggle it on/off. It can also be started
or stopped in real-time.
- Comes with 3 different animation modes - "gradient", "smooth_strobe", and "fast_strobe".
- Comes with 18 built-in patterns and a pattern constructor argument for easy setting.
- Has a `repeat` constructor argument for creating your own patterns or tiling any art.
- Fully reactive - update the loaded ASCII art change patterns in real-time. Will resize automatically when width or height is set to auto.
- Animation settings have a variety of variables to modify, including horizontal, reverse, FPS, and quality.
- Included demo app to showcase the features.

## Demo App

If you have [uv](https://docs.astral.sh/uv/) or [pipx](https://pipx.pypa.io/stable/), you can immediately try the demo app:

```sh
uvx textual-coloromatic
```

```sh
pipx run textual-coloromatic
```

## Documentation

### [Click here for documentation](https://edward-jazzhands.github.io/libraries/textual-coloromatic/docs/)

## Video

<video style="width: 100%; height: auto;" controls loop>
  <source src="https://edward-jazzhands.github.io/assets/textual-coloromatic/demo-0.2.1-handbrake.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

[ ](https://github.com/user-attachments/assets/1140fd13-526c-4bc8-b489-a6e59d9b5252)

## Questions, Issues, Suggestions?

Use the [issues](https://github.com/edward-jazzhands/textual-coloromatic/issues) section for bugs or problems, and post ideas or feature requests on the [TTY group discussion board](https://github.com/orgs/ttygroup/discussions).
