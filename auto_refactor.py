import ast, json, shutil
from pathlib import Path

ROOT = Path('.').resolve()

from utils.get_py_files import get_py_files

from utils.count_lines import count_lines

from utils.parse_functions import parse_functions

from utils.find_function_calls import find_function_calls

from utils.ensure_package import ensure_package

from utils.move_function_to_module import move_function_to_module

from utils.snake_case import snake_case

from utils.main import main

if __name__ == '__main__':
    main()
