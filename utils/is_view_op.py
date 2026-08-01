
def is_view_op(schema: torch._C.FunctionSchema) -> bool:
    if len(schema.arguments) == 0:
        return False
    alias_info = schema.arguments[0].alias_info
    return (alias_info is not None) and (not alias_info.is_write)

