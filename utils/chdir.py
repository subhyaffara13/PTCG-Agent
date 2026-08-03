import os
from pathlib import Path


def chdir(d):
    cwd = os.getcwd()
    try:
        os.chdir(d)
        yield
    finally:
        os.chdir(cwd)


def chdir(target: Path) -> Iterator[None]:
    # Replace with contextlib.chdir in Python 3.11
    dir = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(dir)

