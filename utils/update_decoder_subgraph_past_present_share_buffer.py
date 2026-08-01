
def update_decoder_subgraph_past_present_share_buffer(subg: GraphProto):
    input_past_0 = 3
    output_past_0 = 1
    new_inputs = []
    for i, vi in enumerate(subg.input):
        if i >= input_past_0:
            shape = shape_of(vi)
            vi = onnx.helper.make_tensor_value_info(  # noqa: PLW2901
                vi.name,
                elem_type=vi.type.tensor_type.elem_type,
                shape=[shape[0], shape[1], shape[2], "max_seq_len", shape[4]],
            )
        new_inputs.extend([vi])
    new_inputs.extend([onnx.helper.make_tensor_value_info("past_sequence_length", onnx.TensorProto.INT32, shape=[1])])
    subg.ClearField("input")
    subg.input.extend(new_inputs)

    new_outputs = []
    for i, vi in enumerate(subg.output):
        if i >= output_past_0:
            shape = shape_of(vi)
            vi = onnx.helper.make_tensor_value_info(  # noqa: PLW2901
                vi.name,
                elem_type=vi.type.tensor_type.elem_type,
                shape=[shape[0], shape[1], shape[2], "max_seq_len", shape[4]],
            )
        new_outputs.extend([vi])
    subg.ClearField("output")
    subg.output.extend(new_outputs)

    new_nodes = []
    for node in subg.node:
        new_node = node
        if node.op_type == "Attention":
            kwargs = kwargs_of(node)
            kwargs.update({"past_present_share_buffer": 1})
            nis = []
            nis.extend(node.input)
            while len(nis) < 6:
                nis.extend([""])
            if len(nis) < 7:
                nis.extend(["past_sequence_length"])
            new_node = onnx.helper.make_node("Attention", nis, node.output, name=node.name, **kwargs)
        new_nodes.extend([new_node])
    subg.ClearField("node")
    subg.node.extend(new_nodes)
    return subg

