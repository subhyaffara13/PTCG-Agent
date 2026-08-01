
def has_tensor_arg(schema: _C.FunctionSchema) -> bool:
    """
    Given a schema, returns True if the schema has a Tensor arg.
    A Tensor arg is any arg with a type annotation that might involve Tensor.
    """
    return any(
        (is_tensor_like_type(a.type) or is_tensorlist_like_type(a.type))
        for a in schema.arguments
    )

