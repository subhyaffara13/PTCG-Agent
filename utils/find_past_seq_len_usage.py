
def find_past_seq_len_usage(subg: GraphProto):
    """Correct graph which originally use dim of past_seq_len from input_ids's shape which is fixed to max_seq_len after
       shared past/present buffer

    Args:
        subg (GraphProto): GraphProto of the decoder subgraph
    return:
        tensor_names_to_rename : set of tensor names which is equal to past_sequence_length
        nodes_to_remove : list of node to remove
    """
    tensor_names_to_rename = set()
    nodes_to_remove = []

    graph_input_names = {inp.name: index for index, inp in enumerate(subg.input)}

    input_name_to_nodes = {}
    output_name_to_node = {}
    for node in subg.node:
        for input_name in node.input:
            if input_name:
                if input_name not in input_name_to_nodes:
                    input_name_to_nodes[input_name] = [node]
                else:
                    input_name_to_nodes[input_name].append(node)
        for output_name in node.output:
            if output_name:
                output_name_to_node[output_name] = node

    for node in subg.node:
        # find "past_key_self_0 --> [Transpose(past_key_self_0) --> Reshape(past_key_self_0)] --> Shape(past_key_self_0) --> Gather(*, 2)"
        # where [Transpose(past_key_self_0) --> Reshape(past_key_self_0)] may or may not exist
        if node.op_type == "Gather":
            if not node.input[1] or not node.input[0]:
                continue

            # Find Gather node's index value
            shape_tensor_name, shape_index_name = (node.input[0], node.input[1])
            ini_gather_indices = None
            if "Constant_" in shape_index_name:
                # If shape_index_name refers to a Constant node
                for const_node in subg.node:
                    if const_node.op_type == "Constant" and const_node.output[0] == shape_index_name:
                        ini_gather_indices = const_node.attribute[0].t
                        break
            else:
                # If shape_index_name refers to an initializer
                for tensor in subg.initializer:
                    if tensor.name == shape_index_name:
                        ini_gather_indices = tensor
                        break
            if ini_gather_indices is None:
                continue
            gather_indices_arr = onnx.numpy_helper.to_array(ini_gather_indices)

            if (
                gather_indices_arr.size == 1
                and gather_indices_arr.item() in {1, 2}
                and node.input[0] in output_name_to_node
            ):
                shape_node = output_name_to_node[shape_tensor_name]
                if not (shape_node.op_type == "Shape" and shape_node.input[0]):
                    continue

                if (
                    shape_node.input[0] in graph_input_names
                    and (
                        shape_node.input[0].startswith("past_key_self_")
                        or shape_node.input[0].startswith("past_value_self_")
                    )
                    and gather_indices_arr.item() == 2
                ):
                    # "past_key_self_0 --> Shape(past_key_self_0) --> Gather(*, 2)"
                    tensor_names_to_rename.add(node.output[0])
                    nodes_to_remove.append(node)
                    if len(input_name_to_nodes[shape_node.output[0]]) == 1:
                        nodes_to_remove.append(shape_node)
                        continue

                if shape_node.input[0] not in output_name_to_node:
                    continue
                reshape_node = output_name_to_node[shape_node.input[0]]
                if not (reshape_node.op_type == "Reshape" and reshape_node.input[0]):
                    continue
                transpose_node = output_name_to_node[reshape_node.input[0]]
                if not (transpose_node.op_type == "Transpose" and transpose_node.input[0]):
                    continue

                if (
                    transpose_node.input[0] in graph_input_names
                    and (
                        transpose_node.input[0].startswith("past_key_self_")
                        or transpose_node.input[0].startswith("past_value_self_")
                    )
                    and gather_indices_arr.item() == 1
                ):
                    # "past_key_self_0 --> Transpose(past_key_self_0) --> Reshape(past_key_self_0) --> Shape(past_key_self_0) --> Gather(*, 2)"
                    tensor_names_to_rename.add(node.output[0])
                    nodes_to_remove.extend([node, shape_node, reshape_node])
                    if len(input_name_to_nodes[transpose_node.output[0]]) == 1:
                        nodes_to_remove.append(transpose_node)
                        continue

    return tensor_names_to_rename, nodes_to_remove

