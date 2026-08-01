
def move_initializers(
    graph: GraphProto,
    min_elements: int = 1024,
) -> list[TensorProto]:
    """Remove initializers of a graph, when they have number of elements larger than a threshold.

    Args:
        graph (GraphProto): the graph.
        min_elements (int, optional): minimal number of elements for initializers to be considered. Defaults to 1024.

    Returns:
        List[TensorProto]: initializers that are removed from the graph.
    """
    moved_initializers = []
    for tensor in graph.initializer:
        if not (tensor.dims and sum(tensor.dims) >= min_elements):
            continue
        moved_initializers.append(tensor)

    for initializer in moved_initializers:
        graph.initializer.remove(initializer)

    # Add type info, otherwise ORT will raise error: "input arg (*) does not have type information set by parent node."
    for initializer in moved_initializers:
        shape = onnx.numpy_helper.to_array(initializer).shape
        value_info = onnx.helper.make_tensor_value_info(initializer.name, initializer.data_type, shape)
        graph.value_info.append(value_info)

    return moved_initializers

