
def is_sys_guard(node: nodes.If) -> bool:
    """Return True if IF stmt is a sys.version_info guard.

    >>> import sys
    >>> from typing import Literal
    """
    if isinstance(node.test, nodes.Compare):
        value = node.test.left
        if isinstance(value, nodes.Subscript):
            value = value.value
        if (
            isinstance(value, nodes.Attribute)
            and value.as_string() == "sys.version_info"
        ):
            return True
    elif isinstance(node.test, nodes.Attribute) and node.test.as_string() in {
        "six.PY2",
        "six.PY3",
    }:
        return True
    return False

