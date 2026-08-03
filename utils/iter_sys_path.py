import os
import sys

def iter_sys_path() -> t.Iterator[tuple[str, bool, bool]]:
    if os.name == "posix":

        def strip(x: str) -> str:
            prefix = os.path.expanduser("~")
            if x.startswith(prefix):
                x = f"~{x[len(prefix) :]}"
            return x

    else:

        def strip(x: str) -> str:
            return x

    cwd = os.path.abspath(os.getcwd())
    for item in sys.path:
        path = os.path.join(cwd, item or os.path.curdir)
        yield strip(os.path.normpath(path)), not os.path.isdir(path), path != item

