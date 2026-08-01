
def render_call(fn, args, kwargs):
    str_fn = torch.overrides.resolve_name(fn)
    if str_fn is None:
        str_fn = str(fn)

    str_args: list[str] = []
    with torch._tensor_str.printoptions(threshold=0, edgeitems=0):
        str_args.extend(repr(a) for a in args)
        str_args.extend(f"{k}={repr(v)}" for k, v in kwargs.items())
        r = f"{str_fn}({', '.join(str_args)})"
    return r

