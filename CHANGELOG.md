# Textual-Color-O-Matic Changelog

## [1.0.0] 2025-07-28

### Usage / API changes

- Promoted library to 1.0.0 / stable release.
- Upgraded to Textual 5.0.0.

### Code and project changes

- Renamed Changelog.md to CHANGELOG.md
- Added 2 workflow to .github/workflows:
  - ci-checks.yml - runs Ruff, MyPy, BasedPyright (will add Pytest later)
  - release.yml - Workflow to publish to PyPI and github releases
- Added 2 scripts to .github/scripts:
  - adds .github/scripts/validate_main.sh
  - adds .github/scripts/tag_release.py
- Added 1 new file to root: `ci-requirements.txt` - this is used by the ci-checks.yml workflow to install the dev dependencies.
- Added basedpyright as a dev dependency to help with type checking. Made the `just typecheck` command run it after MyPy and set it to 'strict' mode in the config (added [tool.basedpyright] section to pyproject.toml).
- Replaced build and publish commands in the justfile with a single release command that runs the two above scripts and then pushes the new tag to Github
- Workflow `update-docs.yml` now runs only if the `release.yml` workflow is successful, so it will only update the docs if a new release is made (Still possible to manually run it if needed, should add a 'docs' tag in the future for this purpose).
- Changed the `.python-version` file to use `3.9` instead of `3.12`.
- Deleted the CustomListView class as it is no longer necessary in Textual 5.0.0. (Textual added indexing to the ListView class).

## [0.2.1] (2025-06-19)

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
