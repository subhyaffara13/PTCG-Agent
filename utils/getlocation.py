import os
from pathlib import Path


def getlocation(function, curdir: str | os.PathLike[str] | None = None) -> str:
    function = get_real_func(function)
    fn = Path(inspect.getfile(function))
    lineno = function.__code__.co_firstlineno
    if curdir is not None:
        try:
            relfn = fn.relative_to(curdir)
        except ValueError:
            pass
        else:
            return f"{relfn}:{lineno + 1}"
    return f"{fn}:{lineno + 1}"

