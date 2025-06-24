<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/939446b8-5257-4e2c-b0d9-338cfa4973e5">
  <img src="https://github.com/user-attachments/assets/ce8e2acb-fbba-4c63-8e50-c361d909c6ae">
</picture>

# textual-coloromatic

![badge](https://img.shields.io/badge/Linted-Ruff-blue&logo=ruff)
![badge](https://img.shields.io/badge/Formatted-Black-black)
![badge](https://img.shields.io/badge/Type_checked-MyPy-blue&logo=python)
![badge](https://img.shields.io/badge/Type_checked-Pyright-blue&logo=python)
![badge](https://img.shields.io/badge/License-MIT-blue)
[![Framework: Textual](https://img.shields.io/badge/framework-Textual-5967FF?logo=python)](https://www.textualize.io/)

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

If you have uv or Pipx, you can immediately try the demo app:

```sh
uvx textual-coloromatic
```

```sh
pipx run textual-coloromatic
```

## Documentation

### [Click here for documentation](https://edward-jazzhands.github.io/libraries/textual-coloromatic/)

## Video

https://github.com/user-attachments/assets/863114a0-1cad-4b1e-bfeb-ed04736c4bce

## Questions, issues, suggestions?

Feel free to post an issue.
