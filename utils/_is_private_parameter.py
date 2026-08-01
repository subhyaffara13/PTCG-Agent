
def _is_private_parameter(arg: inspect.Parameter) -> bool:
    return (
        arg.name.startswith("_")
        and not arg.name.startswith("__")
        and arg.default is not inspect.Parameter.empty
    )

