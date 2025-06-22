# Textual-Color-O-Matic Changelog

## 0.2.1 (2025-06-19)

- Removed the logging statements from Coloromatic (forgot to remove them)

## 0.2.0 (2025-06-19) - The Repeating Update

- Added a big new feature, repeating patterns. Colormatic now has a `repeat` argument and reactive attribute of the same name.
- Added a new `pattern` argument. Instead of inputting a string, you can now just set to one of the built-in patterns. This is type-hinted as a string literal to give auto-completion for the available patterns. Setting a pattern will automatically set repeating to True.
- Overhauled demo to show off the new repeating mode with a "Tiling" switch on the controls bar. There's also a new screen to enter a string directly.
- Added a "show child" switch in the demo to demonstrate how the art/pattern in the ColorOmatic can be rendered behind child widgets as a backdrop.
- Added a new `add_directory` method in the ColorOmatic and in the ArtLoader to add custom directories to the file dictionary.
- Added a new `file_dict` property in the ColorOmatic for easy access to the dictionary of all files. This returns a dictionary of all the stored directories (and a list of path objects for each one). These will be the built-in patterns folder and any folders that you have added manually.
- Refactored internals heavily. Now uses `self.auto_refresh` instead of setting an interval timer manually. Also moved logic from the overridden `render_lines` method into the `auto_refresh` method (no longer overriding `render_lines`).
- Created a `_complete_init__` method for finishing initialization.

## 0.1.3 (2025-06-15)

- Added width and height attributes to the Updated message for more compatibility with Textual-Pyfiglet

## 0.1.0 (2025-06-15)

- First alpha release
