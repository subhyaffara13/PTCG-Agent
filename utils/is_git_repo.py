import os
from pathlib import Path


def is_git_repo(dir: str) -> bool:
    """Is the given directory version-controlled with git?"""
    return os.path.exists(os.path.join(dir, ".git"))


def is_git_repo(dir: Path) -> bool:
    """Is the given directory version-controlled with git?"""
    return dir.joinpath('.git').exists()

