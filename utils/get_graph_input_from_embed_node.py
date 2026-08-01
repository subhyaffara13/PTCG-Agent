
def get_graph_input_from_embed_node(onnx_model, embed_node, input_index):
    if input_index >= len(embed_node.input):
        return None

    input = embed_node.input[input_index]
    graph_input = onnx_model.find_graph_input(input)
    if graph_input is None:
        parent_node = onnx_model.get_parent(embed_node, input_index)
        if parent_node is not None and parent_node.op_type == "Cast":
            graph_input = onnx_model.find_graph_input(parent_node.input[0])
    return graph_input

