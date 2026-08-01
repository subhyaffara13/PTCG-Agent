
def get_shape_from_value_info(vi):
    cls_type = vi.type.WhichOneof("value")
    if cls_type is None:
        return None
    if is_sequence(vi.type):
        if vi.type.sequence_type.elem_type.WhichOneof("value") == "tensor_type":
            return get_shape_from_type_proto(vi.type.sequence_type.elem_type)
        else:
            return None
    else:
        return get_shape_from_type_proto(vi.type)

