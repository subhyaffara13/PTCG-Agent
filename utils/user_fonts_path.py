from pathlib import Path


def user_fonts_path() -> Path:
    """:returns: fonts path tied to the user"""
    return PlatformDirs().user_fonts_path

