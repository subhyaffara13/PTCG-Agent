
def _is_mutable_arg(arg: torch._C.Argument) -> bool:
    return arg.alias_info is not None and arg.alias_info.is_write

