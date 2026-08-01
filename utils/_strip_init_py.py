
def _strip_init_py(s: str) -> str:
    suffix = "__init__.py"
    s = s.removesuffix(suffix)
    return _as_posix_path(s)

