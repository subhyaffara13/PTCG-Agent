
def namedtuple_args(schema, args):
    if not isinstance(args, tuple):
        raise AssertionError(f"expected tuple, got {type(args)}")
    tuple_cls = namedtuple_args_cls(schema)
    return tuple_cls(*args)

