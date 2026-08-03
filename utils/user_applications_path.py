from pathlib import Path


def user_applications_path() -> Path:
    """:returns: applications path tied to the user"""
    return PlatformDirs().user_applications_path

