from pathlib import Path


def get_codebase_files():
    files = []
    for ext in ["*.py", "*.cpp", "*.h"]:
        files.extend(list(Path("factory").rglob(ext)))
        files.extend(list(Path("src").rglob(ext)))
    return files

