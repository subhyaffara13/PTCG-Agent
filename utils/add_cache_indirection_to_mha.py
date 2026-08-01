
def add_cache_indirection_to_mha(model: OnnxModel, past_seq_len_name: str):
    # Add past_sequence_length and cache_indirection as inputs to all MultiHeadAttention ops and as inputs to model
    cache_indirection_name = "cache_indirection"
    mha_nodes = list(filter(lambda node: node.op_type == "MultiHeadAttention", model.model.graph.node))
    for node in mha_nodes:
        # MHA op takes the following potential inputs:
        # query, key, value, bias, key_padding_mask, add_qk, past_key, past_value
        while len(node.input) < 8:
            node.input.append("")
        node.input.append(past_seq_len_name)
        node.input.append(cache_indirection_name)

    model.model.graph.input.append(
        onnx.helper.make_tensor_value_info(
            cache_indirection_name, TensorProto.INT32, shape=["batch_size", "beam_width", "max_sequence_length"]
        ),
    )
    model.topological_sort()
    return model

