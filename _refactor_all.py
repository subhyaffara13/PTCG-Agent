"""
Final refactoring script:
- Standalone .py files -> packages (dir with __init__.py + sub-modules)
- Sub-package files -> _prefixed helper extraction
- Large classes: extract methods into helpers
- Large functions: extract body into helpers
"""
import ast
import shutil
import re
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

# Which dirs to scan (all under these)
SCAN_DIRS = [
    "distributed", "router", "tests",
    "run_guided_helpers", "numpy_forward", "run_audit_pipeline",
]

# Directories that are already packages (their files get _prefixed extraction)
PKG_DIRS = set()
for candidate in [
    "run_guided_helpers", "numpy_forward", "run_audit_pipeline",
]:
    p = ROOT / candidate
    if p.exists() and (p / "__init__.py").exists():
        PKG_DIRS.add(p.resolve())


from utils.is_pkg_file import is_pkg_file


from utils.node_text import node_text


from utils.names_from_node import names_from_node


from utils.is_name_main import is_name_main


BUILTINS = set(dir(__builtins__))


from utils.param_names import param_names


from utils.local_names import local_names


from utils.body_refs import body_refs


from utils.make_mod_name import make_mod_name


# ---------------------------------------------------------------------------
#  Refactor: Standalone file -> Package
# ---------------------------------------------------------------------------

from utils.refactor_standalone import refactor_standalone


# ---------------------------------------------------------------------------
#  Refactor: File in sub-package -> _prefixed helpers
# ---------------------------------------------------------------------------

from utils.split_large_def import split_large_def


from utils._split_class import _split_class


from utils._split_function import _split_function


# ---------------------------------------------------------------------------
#  Refactor: file in sub-package -> _prefixed module extraction
# ---------------------------------------------------------------------------

from utils.refactor_pkg_file import refactor_pkg_file


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

from utils.main import main


if __name__ == '__main__':
    main()
