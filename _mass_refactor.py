"""Mass refactoring: split large files (~50 lines) by extracting helper functions/classes."""
import ast
import builtins
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
LINE_LIMIT = 50
BUILTIN_NAMES = set(dir(builtins))

# Files to refactor: priority 1 then 2 then 3 (all > 50 lines in packages with __init__)
# We auto-detect all files > 50 lines inside packages

from utils._find_all_over_50 import _find_all_over_50

from utils._top_level_names import _top_level_names

from utils._class_methods import _class_methods

from utils._extract_function_body_lines import _extract_function_body_lines

from utils.refactor_file import refactor_file

from utils._refactor_class import _refactor_class

from utils._refactor_function import _refactor_function

from utils._identify_blocks import _identify_blocks

from utils._ensure_exports_in_init import _ensure_exports_in_init

from utils.main import main

if __name__ == '__main__':
    main()
