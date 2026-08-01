
def is_tensor_like_type(typ: Any) -> bool:
    return typ == _C.TensorType.get() or typ == _C.OptionalType(_C.TensorType.get())

