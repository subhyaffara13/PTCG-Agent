
def _clean_initializers_helper(graph, model):
    """Clean unused initializers from graph.

    Returns:
        A cleaned graph without unused initializers
        A list of tensor names, which are not produced by this graph and its subgraphes
    """
    requesting_tensor_names = set()
    requesting_tensor_names.update(input_name for node in graph.node for input_name in node.input if input_name)
    requesting_tensor_names.update(g_out.name for g_out in graph.output if g_out.name)

    new_nodes = []
    for node in graph.node:
        new_node = node
        graph_attrs = [
            attr
            for attr in node.attribute
            if attr.type == onnx.AttributeProto.GRAPH or attr.type == onnx.AttributeProto.GRAPHS
        ]
        if graph_attrs:
            kwargs = {}
            for attr in node.attribute:
                new_attribute = {}
                if attr.type == onnx.AttributeProto.GRAPH:
                    (
                        cleaned_sub_graph,
                        sub_requesting_tensor_names,
                    ) = _clean_initializers_helper(attr.g, model)
                    new_attribute = {attr.name: cleaned_sub_graph}
                    requesting_tensor_names.update(sub_requesting_tensor_names)
                elif attr.type == onnx.AttributeProto.GRAPHS:
                    cleaned_graphes = []
                    for subgraph in attr.graphs:
                        (
                            cleaned_sub_graph,
                            sub_requesting_tensor_names,
                        ) = _clean_initializers_helper(subgraph, model)
                        cleaned_graphes.append(cleaned_sub_graph)
                        requesting_tensor_names.update(sub_requesting_tensor_names)
                    new_attribute = {attr.name: cleaned_graphes}
                else:
                    new_attribute = attribute_to_kwarg(attr)
                kwargs.update(new_attribute)
            new_node = onnx_helper.make_node(node.op_type, node.input, node.output, name=node.name, **kwargs)
        new_nodes.append(new_node)

    graph.ClearField("node")
    graph.node.extend(new_nodes)

    requesting_tensor_names.difference_update(output for node in graph.node for output in node.output)

    unused_initializer = []
    for initializer in graph.initializer:
        if initializer.name in requesting_tensor_names:
            requesting_tensor_names.remove(initializer.name)
        else:
            # mark it to remove, remove here directly will cause mis-behavier
            unused_initializer.append(initializer)

    name_to_input = {input.name: input for input in graph.input}
    for initializer in unused_initializer:
        graph.initializer.remove(initializer)
        if initializer.name in name_to_input:
            try:
                graph.input.remove(name_to_input[initializer.name])
            except StopIteration:
                if model.ir_version < 4:
                    print(f"Warning: invalid weight name {initializer.name} found in the graph (not a graph input)")

    requesting_tensor_names.difference_update(input.name for input in graph.input)

    return graph, requesting_tensor_names

