"""Fix syntactically broken generated files and split remaining large files."""
import ast
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

class class_to_parts:
    """Split a large class into sub-modules."""

from utils.is_valid_python import is_valid_python

from utils.fix_and_split import fix_and_split


from utils.main import main

if __name__ == '__main__':
    main()
