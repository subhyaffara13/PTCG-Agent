
def _validate_and_wrap_argnum(argnum: int, num_args: int) -> int:
    if not isinstance(argnum, int):
        raise RuntimeError(f"argnum must be int, got: {type(argnum)}")
    if argnum >= 0 and argnum < num_args:
        return argnum
    if argnum < 0 and argnum >= -num_args:
        return argnum + num_args
    raise RuntimeError(f"Got argnum={argnum}, but only {num_args} positional inputs")

