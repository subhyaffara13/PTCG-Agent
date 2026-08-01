
def _is_tensor_list(x: _C.Value) -> bool:
    x_type = _as_list_type(x.type())
    if x_type is None:
        return False
    return isinstance(x_type.getElementType(), _C.TensorType)

