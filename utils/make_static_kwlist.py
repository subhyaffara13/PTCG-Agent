
def make_static_kwlist(args: list[RuntimeArg]) -> str:
    arg_names = "".join(f'"{arg.name}", ' for arg in args)
    return f"static const char * const kwlist[] = {{{arg_names}0}};"

