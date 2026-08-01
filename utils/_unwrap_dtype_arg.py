
def _unwrap_dtype_arg(arg: DTypeArg) -> DTypeVar | torch.types.Number | str:
    if isinstance(arg, OpsValue):
        return arg.value
    return arg

