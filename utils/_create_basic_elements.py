from typing import Any, List, Set, Tuple

def _create_basic_elements(
    value: Iterable[Any], node: List | Set | Tuple
) -> list[NodeNG]:
    """Create a list of nodes to function as the elements of a new node."""
    elements: list[NodeNG] = []
    for element in value:
        # NOTE: avoid accessing any attributes of element in the loop.
        element_node = const_factory(element)
        element_node.parent = node
        elements.append(element_node)
    return elements

