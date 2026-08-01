
def python_qualified_identifier(value: str) -> bool:
    """
    Python "dotted identifier", i.e. a sequence of :obj:`python_identifier`
    concatenated with ``"."`` (e.g.: ``package.module.submodule``).
    """
    if value.startswith(".") or value.endswith("."):
        return False
    return all(python_identifier(m) for m in value.split("."))

