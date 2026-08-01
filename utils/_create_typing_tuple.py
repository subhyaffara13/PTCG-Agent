
def _create_typing_tuple(argz, *args): #NOTE: workaround python/cpython#94245
    if not argz:
        return typing.Tuple[()].copy_with(())
    if argz == ((),):
        return typing.Tuple[()]
    return typing.Tuple[argz]

