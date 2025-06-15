"""art_loader.py"""

# Python imports
from __future__ import annotations
from pathlib import Path

# from textual.widget import Widget
import textual_coloromatic.art


class ArtLoader:

    def __init__(self, directories: list[Path] | None = None) -> None:
        """
        Initialize the art loader with one or more art directories.

        Args:
            directories: List of directories to search for art files.
        """
        super().__init__()
        self.display = False
        self.directories: list[Path] = []

        try:
            pkg_path: list[str] = getattr(textual_coloromatic.art, "__path__")
        except AttributeError as e:
            raise AttributeError(
                "Could not find the package path for textual_coloromatic.art. "
                "Ensure that textual_coloromatic.art is a valid package."
            ) from e

        default_path = Path(pkg_path[0])
        if not default_path.exists():
            raise FileNotFoundError(f"Art directory not found: {default_path}")

        self.directories.extend([default_path])
        if directories:
            self.directories.extend(directories)

    def load_art_file_list(self) -> list[Path]:
        """
        Scan all art directories for .txt files and return a list of their paths.
        """
        accepted_extensions = {".txt", ".md", ".art"}

        art_files: list[Path] = []
        for directory in self.directories:
            if not directory.exists():
                continue
            for file in directory.iterdir():
                if file.is_file() and file.suffix in accepted_extensions:
                    art_files.append(file)

        if not art_files:
            raise FileNotFoundError("No art files found in the specified directories.")

        return art_files

    @staticmethod
    def extract_art_at_path(path: Path) -> list[str]:
        """
        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error reading the file.
            ValueError: If the file is empty or contains only whitespace.
        """

        # the path objects will be pointing to .txt files
        # we just need to read those files and extract the contents.

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        try:
            with path.open(encoding="utf-8") as file:
                art_content = file.read()
        except Exception as e:
            raise IOError(f"Error reading file {path}: {e}")
        if not art_content.strip():
            raise ValueError(f"File {path} is empty or contains only whitespace.")

        # we need to remove the header metadata from the art content
        # if the file has any, which is usually the case.
        # The header metadata is separated by a line with only dashes.

        lines: list[str] = art_content.splitlines()
        header_end_index = 0
        for index, line in enumerate(lines):
            current_index = index + 1
            if line.strip().startswith("---"):
                header_end_index = current_index
                break

        new_list: list[str] = lines[header_end_index:]
        if not art_content:
            raise ValueError(f"File {path} has no content after header.")

        return new_list
