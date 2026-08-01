"""Split large C++ files into ~50-line modules with proper cross-file handling."""
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

SKIP_WORDS = {'if', 'else', 'while', 'for', 'switch', 'catch', 'try', 'case', 'return',
              'delete', 'new', 'sizeof', 'throw', 'template', 'class', 'struct',
              'enum', 'namespace', 'using', 'typedef', 'public:', 'private:', 'protected:'}

from utils.find_closing_brace import find_closing_brace

from utils.merge_sig_lines import merge_sig_lines

from utils.extract_globals import extract_globals

from utils.extract_static_func_decls import extract_static_func_decls

from utils.find_functions import find_functions

from utils.refactor_cpp import refactor_cpp

from utils.update_cmakelists import update_cmakelists

from utils.main import main

if __name__ == '__main__':
    main()
