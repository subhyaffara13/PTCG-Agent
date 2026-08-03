import re

def parse_signature(sig: str) -> tuple[str, list[str], list[str]] | None:
    """Split function signature into its name, positional an optional arguments.

    The expected format is "func_name(arg, opt_arg=False)". Return the name of function
    and lists of positional and optional argument names.
    """
    m = re.match(r"([.a-zA-Z0-9_]+)\(([^)]*)\)", sig)
    if not m:
        return None
    name = m.group(1)
    name = name.split(".")[-1]
    arg_string = m.group(2)
    if not arg_string.strip():
        # Simple case -- no arguments.
        return name, [], []

    args = [arg.strip() for arg in arg_string.split(",")]
    positional = []
    optional = []
    i = 0
    while i < len(args):
        # Accept optional arguments as in both formats: x=None and [x].
        if args[i].startswith("[") or "=" in args[i]:
            break
        positional.append(args[i].rstrip("["))
        i += 1
        if args[i - 1].endswith("["):
            break
    while i < len(args):
        arg = args[i]
        arg = arg.strip("[]")
        arg = arg.split("=")[0]
        optional.append(arg)
        i += 1
    return name, positional, optional

