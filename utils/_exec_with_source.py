
def _exec_with_source(src: str, globals: dict[str, Any], co_fields=None):
    key = _loader.cache(src, globals, co_fields)
    exec(compile(src, key, "exec"), globals)

