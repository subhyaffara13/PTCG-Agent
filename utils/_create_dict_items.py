
def _create_dict_items(
    values: Mapping[Any, Any], node: Dict
) -> list[tuple[SuccessfulInferenceResult, SuccessfulInferenceResult]]:
    """Create a list of node pairs to function as the items of a new dict node."""
    elements: list[tuple[SuccessfulInferenceResult, SuccessfulInferenceResult]] = []
    for key, value in values.items():
        # NOTE: avoid accessing any attributes of both key and value in the loop.
        key_node = const_factory(key)
        key_node.parent = node
        value_node = const_factory(value)
        value_node.parent = node
        elements.append((key_node, value_node))
    return elements

