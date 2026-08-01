
def get_elem_type_from_type_proto(type_proto):
    if is_sequence(type_proto):
        return type_proto.sequence_type.elem_type.tensor_type.elem_type
    else:
        return type_proto.tensor_type.elem_type

