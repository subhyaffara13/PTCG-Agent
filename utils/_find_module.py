import os

def _find_module(
    module_name: str, package_dir: Mapping[str, str] | None, root_dir: StrPath
) -> str | None:
    """Find the path to the module named ``module_name``,
    considering the ``package_dir`` in the build configuration and ``root_dir``.

    >>> tmp = getfixture('tmpdir')
    >>> _ = tmp.ensure("a/b/c.py")
    >>> _ = tmp.ensure("a/b/d/__init__.py")
    >>> r = lambda x: x.replace(str(tmp), "tmp").replace(os.sep, "/")
    >>> r(_find_module("a.b.c", None, tmp))
    'tmp/a/b/c.py'
    >>> r(_find_module("f.g.h", {"": "1", "f": "2", "f.g": "3", "f.g.h": "a/b/d"}, tmp))
    'tmp/a/b/d/__init__.py'
    """
    path_start = find_package_path(module_name, package_dir or {}, root_dir)
    candidates = chain.from_iterable(
        (f"{path_start}{ext}", os.path.join(path_start, f"__init__{ext}"))
        for ext in all_suffixes()
    )
    return next((x for x in candidates if os.path.isfile(x)), None)

