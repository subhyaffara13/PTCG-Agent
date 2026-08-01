
def _is_tensor_constructor(func: OpOverload) -> bool:
    if not isinstance(func, OpOverload):
        raise AssertionError(f"func must be an OpOverload, got {type(func)}")
    schema = func._schema
    if any(contains_tensor_types(arg.type) for arg in schema.arguments):
        return False
    # TODO: no real reason to restrict multiple outputs
    return (
        len(schema.returns) == 1 and schema.returns[0].type is torch._C.TensorType.get()
    )

