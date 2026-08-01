
def _check_generate_dataclass_init(node: nodes.ClassDef) -> bool:
    """Return True if we should generate an __init__ method for node.

    This is True when:
        - node doesn't define its own __init__ method
        - the dataclass decorator was called *without* the keyword argument init=False
    """
    if "__init__" in node.locals:
        return False

    found = None

    for decorator_attribute in node.decorators.nodes:
        if not isinstance(decorator_attribute, nodes.Call):
            continue

        if _looks_like_dataclass_decorator(decorator_attribute):
            found = decorator_attribute

    if found is None:
        return True

    # Check for keyword arguments of the form init=False
    return not any(
        keyword.arg == "init"
        and keyword.value.bool_value() is False  # type: ignore[union-attr] # value is never None
        for keyword in found.keywords
    )

