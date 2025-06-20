# Textual-Color-O-Matic Changelog

## 0.2.0 (2025-06-19) - The Repeating Update

- Added a big new feature, repeating patterns. Colormatic now has a `repeat` argument and reactive attribute of the same name.

- Refactored internals to use `self.auto_refresh` instead of setting an interval timer manually. Also moved logic from the overridden `render_lines` method into the `auto_refresh` method (no longer overriding `render_lines`).
- Refactored the `__init__` method to be faster and created a `_complete_init__` method for finishing initialization.

## 0.1.3 (2025-06-15)

- Added width and height attributes to the Updated message for more compatibility with Textual-Pyfiglet

## 0.1.0 (2025-06-15)

- First alpha release
