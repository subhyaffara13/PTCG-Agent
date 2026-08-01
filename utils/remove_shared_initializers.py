
def remove_shared_initializers(
    graph1: GraphProto,
    graph2: GraphProto,
    shared_prefix: str = "shared_",
    min_elements: int = 1024,
    signature_cache1: dict | None = None,
    signature_cache2: dict | None = None,
):
    """Remove initializers with same value from two graphs.

    Args:
        graph1 (GraphProto): the first graph to process
        graph2 (GraphProto): the second graph to process
        shared_prefix (str): add prefix to the shared initializers among two graphs
        min_elements (int, optional): minimal number of elements for initializers to be considered. Defaults to 1024.
        signature_cache1 (dict): Optional dictionary to store data signatures of tensors in graph1 in order to speed up comparison
        signature_cache2 (dict): Optional dictionary to store data signatures of tensors in graph2 in order to speed up comparison
    """

    mapping_initializers_1 = {}
    mapping_initializers_2 = {}
    shared_initializers_1 = []
    shared_initializers_2 = []
    shared_initializers_names = []

    for initializer1 in graph1.initializer:
        if not (initializer1.dims and sum(initializer1.dims) >= min_elements):
            continue

        for initializer2 in graph2.initializer:
            if not (initializer2.dims and sum(initializer2.dims) >= min_elements):
                continue

            if OnnxModel.has_same_value(initializer1, initializer2, signature_cache1, signature_cache2):
                mapping_initializers_1[initializer1.name] = shared_prefix + initializer2.name
                shared_initializers_1.append(initializer1)

                if initializer2.name not in mapping_initializers_2:
                    shared_name = shared_prefix + initializer2.name
                    mapping_initializers_2[initializer2.name] = shared_name
                    shared_initializers_2.append(initializer2)
                    shared_initializers_names.append(shared_name)
                break

    logger.debug(f"shared initializers:{shared_initializers_names}")

    # Make sure new name does not exist in graph 1
    for node in graph1.node:
        for j in range(len(node.input)):
            if node.input[j] in shared_initializers_names:
                raise RuntimeError(f"name is found in graph 1: {node.input[j]}")

    # Make sure new name does not exist in graph 2
    for node in graph2.node:
        for j in range(len(node.input)):
            if node.input[j] in shared_initializers_names:
                raise RuntimeError(f"name is found in graph 2: {node.input[j]}")

    # Remove shared initializers from graph 2
    for initializer in shared_initializers_2:
        graph2.initializer.remove(initializer)

    # Rename value info for old names in graph 2
    for value_info in graph2.value_info:
        if value_info.name in mapping_initializers_2:
            value_info.name = mapping_initializers_2[value_info.name]

    # Rename nodes inputs in graph 2:
    for node in graph2.node:
        for j in range(len(node.input)):
            if node.input[j] in mapping_initializers_2:
                new_name = mapping_initializers_2[node.input[j]]
                logger.debug(f"graph 2 rename node {node.name} input {j} from {node.input[j]} to {new_name}")
                node.input[j] = new_name

    #  Remove shared initializers from graph 1
    for initializer in shared_initializers_1:
        graph1.initializer.remove(initializer)

    # Rename value info for old names in graph 1
    for value_info in graph1.value_info:
        if value_info.name in mapping_initializers_1:
            value_info.name = mapping_initializers_1[value_info.name]

    # Rename nodes inputs in graph 1:
    for node in graph1.node:
        for j in range(len(node.input)):
            if node.input[j] in mapping_initializers_1:
                new_name = mapping_initializers_1[node.input[j]]
                logger.debug(f"graph 1 rename node {node.name} input {j} from {node.input[j]} to {new_name}")
                node.input[j] = new_name

    # Rename shared initializers in graph 2
    for initializer in shared_initializers_2:
        initializer.name = mapping_initializers_2[initializer.name]

    for initializer in shared_initializers_2:
        shape = onnx.numpy_helper.to_array(initializer).shape
        value_info = onnx.helper.make_tensor_value_info(initializer.name, initializer.data_type, shape)
        # Need add value_info for initializers moved to parent graph. Otherwise, ORT will fail.
        graph1.value_info.append(value_info)
        graph2.value_info.append(value_info)

    return shared_initializers_2

