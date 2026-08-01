"""Split large Python files into ~50-line packages with proper cross-references."""
import ast
import builtins
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

BUILTIN_NAMES = set(dir(builtins))

from utils._is_name_main_check import _is_name_main_check

from utils._names_from_node import _names_from_node

from utils._func_param_names import _func_param_names

from utils.get_local_names import get_local_names

from utils.get_body_refs_for_funcs import get_body_refs_for_funcs

from utils.refactor_file import refactor_file

from utils.main import main

if __name__ == '__main__':
    main()
