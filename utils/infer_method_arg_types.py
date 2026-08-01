
def infer_method_arg_types(
    name: str, self_var: str = "self", arg_names: list[str] | None = None
) -> list[ArgSig] | None:
    """Infer argument types for known special methods"""
    args: list[ArgSig] | None = None
    if name.startswith("__") and name.endswith("__"):
        if arg_names and len(arg_names) >= 1 and arg_names[0] == "self":
            arg_names = arg_names[1:]

        name = name[2:-2]
        if name == "exit":
            if arg_names is None:
                arg_names = ["type", "value", "traceback"]
            if len(arg_names) == 3:
                arg_types = [
                    "type[BaseException] | None",
                    "BaseException | None",
                    "types.TracebackType | None",
                ]
                args = [
                    ArgSig(name=arg_name, type=arg_type)
                    for arg_name, arg_type in zip(arg_names, arg_types)
                ]
    if args is not None:
        return [ArgSig(name=self_var)] + args
    return None

