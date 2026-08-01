
def method_name_sort_key(name: str) -> tuple[int, str]:
    """Sort methods in classes in a typical order.

    I.e.: constructor, normal methods, special methods.
    """
    if name in ("__new__", "__init__"):
        return 0, name
    if name.startswith("__") and name.endswith("__"):
        return 2, name
    return 1, name

