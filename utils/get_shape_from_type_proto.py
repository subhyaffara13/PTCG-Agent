
def get_shape_from_type_proto(type_proto):
    assert not is_sequence(type_proto)
    if type_proto.tensor_type.HasField("shape"):
        return [get_dim_from_proto(d) for d in type_proto.tensor_type.shape.dim]
    else:
        return None  # note no shape is different from shape without dim (scalar)


def get_shape_from_type_proto(type_proto):
    return [get_dim_from_type_proto(d) for d in type_proto.tensor_type.shape.dim]

