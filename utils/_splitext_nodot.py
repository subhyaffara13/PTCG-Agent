import os

def _splitext_nodot(basename: str) -> tuple[str, str]:
    root, ext = os.path.splitext(basename)
    if ext:
        ext = ext[1:]
    return root, ext

