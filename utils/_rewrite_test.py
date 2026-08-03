import os
from pathlib import Path


def _rewrite_test(fn: Path, config: Config) -> tuple[os.stat_result, types.CodeType]:
    """Read and rewrite *fn* and return the code object."""
    stat = os.stat(fn)
    source = fn.read_bytes()
    strfn = str(fn)
    tree = ast.parse(source, filename=strfn)
    rewrite_asserts(tree, source, strfn, config)
    co = compile(tree, strfn, "exec", dont_inherit=True)
    return stat, co

