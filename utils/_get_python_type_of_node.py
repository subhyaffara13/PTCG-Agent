from typing import Callable

def _get_python_type_of_node(node: nodes.NodeNG) -> str | None:
    pytype: Callable[[], str] | None = getattr(node, "pytype", None)
    if callable(pytype):
        return pytype()
    return None

