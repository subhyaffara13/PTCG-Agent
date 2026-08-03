from typing import Any

def _linecache_and_compile(
    script: str,
    filename: str,
    globs: dict[str, Any] | None,
    locals: Mapping[str, object] | None = None,
) -> dict[str, Any]:
    """
    Cache the script with _linecache_, compile it and return the _locals_.
    """

    locs = {} if locals is None else locals

    # In order of debuggers like PDB being able to step through the code,
    # we add a fake linecache entry.
    count = 1
    base_filename = filename
    while True:
        linecache_tuple = (
            len(script),
            None,
            script.splitlines(True),
            filename,
        )
        old_val = linecache.cache.setdefault(filename, linecache_tuple)
        if old_val == linecache_tuple:
            break

        filename = f"{base_filename[:-1]}-{count}>"
        count += 1

    _compile_and_eval(script, globs, locs, filename)

    return locs

