
def get_load_global_name(op: CallC) -> str | None:
    name = op.function_name
    if name == "CPyDict_GetItem":
        arg = op.args[0]
        if (
            isinstance(arg, LoadStatic)
            and arg.namespace == "static"
            and arg.identifier == "globals"
            and isinstance(op.args[1], LoadLiteral)
        ):
            return str(op.args[1].value)
    return None

