import sys
from pathlib import Path


def verify_compatibility(dir_path: Path):
    if dir_path.exists():
        import ast
        for py_file in dir_path.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                print(f"CRITICAL: SyntaxError in {py_file.name}: {e}")
                sys.exit(1)
            for node in ast.walk(tree):
                if isinstance(node, ast.JoinedStr):
                    for val in node.values:
                        if isinstance(val, ast.FormattedValue):
                            expr_str = ast.unparse(val.value)
                            if "'" in expr_str or '"' in expr_str:
                                print(f"CRITICAL: Python 3.11 compatibility error in {py_file.name}: f-string expression contains quotes: {{{expr_str}}}")
                                sys.exit(1)

