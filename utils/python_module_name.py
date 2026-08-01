
def python_module_name(value: str) -> bool:
    """Module name that can be used in an ``import``-statement in Python.
    See :obj:`python_qualified_identifier`.
    """
    return python_qualified_identifier(value)

