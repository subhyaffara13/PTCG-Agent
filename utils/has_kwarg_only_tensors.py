
def has_kwarg_only_tensors(schema: _C.FunctionSchema):
    for a in schema.arguments:
        if not (is_tensor_like_type(a.type) or is_tensorlist_like_type(a.type)):
            continue
        if not a.kwarg_only:
            continue
        return True
    return False

