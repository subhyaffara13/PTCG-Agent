"""Final pass: split remaining files with single large defs by extracting methods/blocks."""
import ast
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

from utils._make_mod_name import _make_mod_name

from utils.split_large_function import split_large_function

from utils.node_text import node_text

from utils.split_large_class import split_large_class


from utils.refactor_file import refactor_file

from utils.main import main

if __name__ == '__main__':
    main()
