
def update_io_to_channel_last(
    model: onnx.ModelProto,
    inputs_to_update: list[str] | None,
    outputs_to_update: list[str] | None,
    transpose_node_name_prefix: str = "Transpose_channel_",
    transpose_node_name_start_suffix: int = 0,
):
    inputs_to_update = set(inputs_to_update or [])
    outputs_to_update = set(outputs_to_update or [])

    if not inputs_to_update and not outputs_to_update:
        return

    graph = model.graph
    orig_graph_inputs = {ginput.name: ginput for ginput in graph.input}
    orig_graph_outputs = {goutput.name: goutput for goutput in graph.output}

    # Check that the user passed in actual input and output names.
    for input_name in inputs_to_update:
        if input_name not in orig_graph_inputs:
            raise ValueError(f"{input_name} is not a graph input")

    for output_name in outputs_to_update:
        if output_name not in orig_graph_outputs:
            raise ValueError(f"{output_name} is not a graph output")

    orig_tensor_names = set()
    orig_tensor_names.update(set(orig_graph_inputs))
    orig_tensor_names.update(set(orig_graph_outputs))
    orig_tensor_names.update(input_name for node in graph.node for input_name in node.input if input_name)

    # Maps original input (or output) name to its updated name used within the graph.
    io_map = InputOutputNameMap(orig_tensor_names, orig_graph_inputs, orig_graph_outputs)

    # Update each node's inputs/outputs to use the transposed versions.
    for node in graph.node:
        for i in range(len(node.input)):
            if node.input[i] and node.input[i] in inputs_to_update:
                node.input[i] = io_map.get_new_name(node.input[i])
            elif node.input[i] and node.input[i] in outputs_to_update:
                node.input[i] = io_map.get_new_name(node.input[i])

        for i in range(len(node.output)):
            if node.output[i] in outputs_to_update:
                node.output[i] = io_map.get_new_name(node.output[i])

    # Update graph inputs to channel-last and a Transpose (to channel-first) after each.
    for g_input_name in inputs_to_update:
        g_input = orig_graph_inputs[g_input_name]

        if not g_input.type.HasField("tensor_type") or not g_input.type.tensor_type.HasField("shape"):
            raise ValueError(f"Expected input {g_input.name} to have a tensor_type with a shape")

        input_shape = g_input.type.tensor_type.shape
        input_rank = len(input_shape.dim)

        if input_rank < 3:
            raise ValueError(f"Expected input {g_input.name} to be of rank >= 3")

        channel_dim = onnx.TensorShapeProto.Dimension()
        channel_dim.CopyFrom(input_shape.dim[1])
        for i in range(1, input_rank - 1):
            input_shape.dim[i].CopyFrom(input_shape.dim[i + 1])
        input_shape.dim[input_rank - 1].CopyFrom(channel_dim)

        transpose_perm = list(range(input_rank))
        for i in range(input_rank):
            transpose_perm[i] = i if i < 1 else i - 1
        transpose_perm[1] = input_rank - 1

        transpose_node = onnx.helper.make_node(
            "Transpose",
            name=f"{transpose_node_name_prefix}{transpose_node_name_start_suffix!s}",
            inputs=[g_input.name],
            outputs=[io_map.get_new_name(g_input.name)],
            perm=transpose_perm,
        )
        transpose_node_name_start_suffix += 1

        graph.node.extend([transpose_node])

    # Update graph outputs to channel-last and a Transpose (from channel-first) before each.
    for g_output_name in outputs_to_update:
        g_output = orig_graph_outputs[g_output_name]
        if not g_output.type.HasField("tensor_type") or not g_output.type.tensor_type.HasField("shape"):
            raise ValueError(f"Expected output {g_output.name} to have a tensor_type with a shape")

        output_shape = g_output.type.tensor_type.shape
        output_rank = len(output_shape.dim)

        if output_rank < 3:
            raise ValueError(f"Expected output {g_output.name} to be of rank >= 3")

        channel_dim = onnx.TensorShapeProto.Dimension()
        channel_dim.CopyFrom(output_shape.dim[1])
        for i in range(1, output_rank - 1):
            output_shape.dim[i].CopyFrom(output_shape.dim[i + 1])
        output_shape.dim[output_rank - 1].CopyFrom(channel_dim)

        transpose_perm = list(range(output_rank))
        for i in range(output_rank):
            transpose_perm[i] = i if i == 0 else i + 1
        transpose_perm[output_rank - 1] = 1

        transpose_node = onnx.helper.make_node(
            "Transpose",
            name=f"{transpose_node_name_prefix}{transpose_node_name_start_suffix!s}",
            inputs=[io_map.get_new_name(g_output.name)],
            outputs=[g_output.name],
            perm=transpose_perm,
        )
        transpose_node_name_start_suffix += 1

        graph.node.extend([transpose_node])

    graph.value_info.extend(io_map.new_value_infos)

