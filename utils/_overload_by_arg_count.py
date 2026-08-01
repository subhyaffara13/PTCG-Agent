
def _overload_by_arg_count(fn):
    @functools.wraps(fn)
    def wrapper(g, *args):
        overloads = fn(g, *args)
        for overload in overloads:
            arg_descriptors = overload._arg_descriptors
            if len(arg_descriptors) == len(args):
                return overload(g, *args)
        return _unimplemented(f"aten::{fn.__name__}", f"with {len(args)} arguments")

    return wrapper

