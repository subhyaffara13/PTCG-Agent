
def accepts_at_least_one_tensor_input(schema: FunctionSchema) -> bool:
    return any(a.type.is_tensor_like() for a in schema.arguments.flat_all)

