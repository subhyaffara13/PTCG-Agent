
def python_module_name_relaxed(value: str) -> bool:
    """Similar to :obj:`python_module_name`, but relaxed to also accept
    dash characters (``-``) and cover special cases like ``pip-run``.

    It is recommended, however, that beginners avoid dash characters,
    as they require advanced knowledge about Python internals.

    The following are disallowed:

    * names starting/ending in dashes,
    * names ending in ``-stubs`` (potentially collide with :obj:`pep561_stub_name`).
    """
    if value.startswith("-") or value.endswith("-"):
        return False
    if value.endswith("-stubs"):
        return False  # Avoid collision with PEP 561
    return python_module_name(value.replace("-", "_"))

