
def maybe_strip_cls(name: str, args: list[nodes.Argument]) -> list[nodes.Argument]:
    if args and name in ("__init_subclass__", "__class_getitem__"):
        # These are implicitly classmethods. If the stub chooses not to have @classmethod, we
        # should remove the cls argument
        if args[0].variable.name == "cls":
            return args[1:]
    return args

