
def is_sequence_type(typ: type) -> bool:
    origin = get_origin(typ) or typ
    return origin == typing_extensions.Sequence or origin == typing.Sequence or origin == _c_abc.Sequence

