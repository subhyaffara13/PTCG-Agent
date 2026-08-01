
def _sanitize_module_name(name: str) -> str:
    r"""
    Tries to sanitize a module name so that it can be used as a Python module.

    The following transformations are applied:

    1. Replace `.` in module names with `_dot_`.
    2. Replace `-` in module names with `_hyphen_`.
    3. If the module name starts with a digit, prepend it with `_`.
    4. Warn if the sanitized name is a Python reserved keyword or not a valid identifier.

    If the input name is already a valid identifier, it is returned unchanged.
    """
    # We not replacing `\W` characters with `_` to avoid collisions. Because `_` is a very common
    # separator used in module names, replacing `\W` with `_` would create too many collisions.
    # Once a module is imported, it is cached in `sys.modules` and the second import would return
    # the first module, which might not be the expected behavior if name collisions happen.
    new_name = name.replace(".", "_dot_").replace("-", "_hyphen_")
    if new_name and new_name[0].isdigit():
        new_name = f"_{new_name}"
    if keyword.iskeyword(new_name):
        logger.warning(
            f"The module name {new_name} (originally {name}) is a reserved keyword in Python. "
            "Please rename the original module to avoid import issues."
        )
    elif not new_name.isidentifier():
        logger.warning(
            f"The module name {new_name} (originally {name}) is not a valid Python identifier. "
            "Please rename the original module to avoid import issues."
        )
    return new_name

