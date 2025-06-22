"""art_loader.py"""

# Python imports
from __future__ import annotations
from pathlib import Path


class ArtLoader:

    def __init__(self, directories: list[Path]) -> None:
        """
        Initialize the art loader with one or more art directories.

        Args:
            directories: List of directories to search for art files.
        """
        super().__init__()

        self.display = False
        self.directories: list[Path] = directories
        self.file_dict = self.load_file_dict()
        """String (key) is the directory name. The value is a list of path objects for each .txt file
        in that directory."""

    def load_file_dict(self) -> dict[str, list[Path]]:
        """Scan all file directories for .txt files. Returns a dict with each directory as
        the key and the value is a list of Path objects (one path object for each .txt file)"""
        accepted_extensions = {".txt"}

        paths_dict: dict[str, list[Path]] = {}
        for directory in self.directories:
            files: list[Path] = []
            if not directory.exists():
                continue
            for file in directory.iterdir():
                if file.is_file() and file.suffix in accepted_extensions:
                    files.append(file)
            paths_dict[directory.name] = files

        return paths_dict

    def add_directory(self, directory: Path) -> None:
        """
        Add a new directory to the art loader.

        Args:
            directory: The directory to add.
        """
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Invalid directory: {directory}")
        self.directories.append(directory)
        self.file_dict = self.load_file_dict()

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
