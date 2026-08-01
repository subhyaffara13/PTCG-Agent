
def extract_element_types(inferred_types: set[InferenceResult]) -> set[nodes.NodeNG]:
    """Extract element types in case the inferred type is a container.

    This function checks if the inferred type is a container type (like list, dict, etc.)
    and extracts the element type(s) from it. If the inferred type is a direct type (like a class),
    it adds that type directly to the set of element types it returns.
    """
    element_types = set()

    for inferred_type in inferred_types:
        if isinstance(inferred_type, nodes.Subscript):
            slice_node = inferred_type.slice

            # Handle both Tuple (dict[K,V]) and single element (list[T])
            elements = (
                slice_node.elts if isinstance(slice_node, nodes.Tuple) else [slice_node]
            )

            for elt in elements:
                if isinstance(elt, (nodes.Name, nodes.ClassDef)):
                    element_types.add(elt)
        else:
            element_types.add(inferred_type)

    return element_types

