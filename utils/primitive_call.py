
def primitive_call(desc: CFunctionDescription, args: list[Value], line: int) -> CallC:
    return CallC(
        desc.c_function_name,
        [],
        desc.return_type,
        desc.steals,
        desc.is_borrowed,
        desc.error_kind,
        line,
        dependencies=desc.dependencies,
    )

