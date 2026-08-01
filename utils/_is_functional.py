
def _is_functional(schema: torch._C.FunctionSchema) -> bool:
    """
    A schema is functional if no argument is written to and the name doesn't
    end with '_'.
    """
    op_name = schema.name.split("::")[-1]
    if op_name.endswith("_"):
        return False
    return not any(arg.is_write for arg in schema.arguments)

