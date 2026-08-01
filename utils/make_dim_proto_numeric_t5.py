
def make_dim_proto_numeric_t5(model, config):
    """Make dim_proto numeric.

    Args:
        model: T5 encoder and decoder model.
        config: T5 config.
    """
    sequence_length = str(1)
    num_heads = str(config.num_heads)
    hidden_size = str(config.d_model)
    head_size = str(config.d_kv)

    for tensor in model.graph.output:
        for dim_proto in tensor.type.tensor_type.shape.dim:
            if dim_proto.HasField("dim_param") and dim_proto.dim_param in [
                sequence_length,
                num_heads,
                hidden_size,
                head_size,
            ]:
                dim_value = int(dim_proto.dim_param)
                dim_proto.Clear()
                dim_proto.dim_value = dim_value

    for tensor in model.graph.input:
        for dim_proto in tensor.type.tensor_type.shape.dim:
            if dim_proto.HasField("dim_param") and dim_proto.dim_param in [
                sequence_length,
                num_heads,
                hidden_size,
                head_size,
            ]:
                dim_value = int(dim_proto.dim_param)
                dim_proto.Clear()
                dim_proto.dim_value = dim_value

