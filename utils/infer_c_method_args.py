
def infer_c_method_args(
    name: str, self_var: str = "self", arg_names: list[str] | None = None
) -> list[ArgSig]:
    args: list[ArgSig] | None = None
    if name.startswith("__") and name.endswith("__"):
        name = name[2:-2]
        if name in (
            "hash",
            "iter",
            "next",
            "sizeof",
            "copy",
            "deepcopy",
            "reduce",
            "getinitargs",
            "int",
            "float",
            "trunc",
            "complex",
            "bool",
            "abs",
            "bytes",
            "dir",
            "len",
            "reversed",
            "round",
            "index",
            "enter",
        ):
            args = []
        elif name == "getitem":
            args = [ArgSig(name="index")]
        elif name == "setitem":
            args = [ArgSig(name="index"), ArgSig(name="object")]
        elif name in ("delattr", "getattr"):
            args = [ArgSig(name="name")]
        elif name == "setattr":
            args = [ArgSig(name="name"), ArgSig(name="value")]
        elif name == "getstate":
            args = []
        elif name == "setstate":
            args = [ArgSig(name="state")]
        elif name in ("eq", "ne", "lt", "le", "gt", "ge"):
            args = [ArgSig(name="other", type="object")]
        elif name in (
            "add",
            "radd",
            "sub",
            "rsub",
            "mul",
            "rmul",
            "mod",
            "rmod",
            "floordiv",
            "rfloordiv",
            "truediv",
            "rtruediv",
            "divmod",
            "rdivmod",
            "pow",
            "rpow",
            "xor",
            "rxor",
            "or",
            "ror",
            "and",
            "rand",
            "lshift",
            "rlshift",
            "rshift",
            "rrshift",
            "contains",
            "delitem",
            "iadd",
            "iand",
            "ifloordiv",
            "ilshift",
            "imod",
            "imul",
            "ior",
            "ipow",
            "irshift",
            "isub",
            "itruediv",
            "ixor",
        ):
            args = [ArgSig(name="other")]
        elif name in ("neg", "pos", "invert"):
            args = []
        elif name == "get":
            args = [ArgSig(name="instance"), ArgSig(name="owner")]
        elif name == "set":
            args = [ArgSig(name="instance"), ArgSig(name="value")]
        elif name == "reduce_ex":
            args = [ArgSig(name="protocol")]
        elif name == "exit":
            args = [
                ArgSig(name="type", type="type[BaseException] | None"),
                ArgSig(name="value", type="BaseException | None"),
                ArgSig(name="traceback", type="types.TracebackType | None"),
            ]
    if args is None:
        args = infer_method_arg_types(name, self_var, arg_names)
    else:
        args = [ArgSig(name=self_var)] + args
    if args is None:
        args = [ArgSig(name="*args"), ArgSig(name="**kwargs")]
    return args

