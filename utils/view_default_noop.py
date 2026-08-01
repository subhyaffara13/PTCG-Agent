
def view_default_noop(arg, size):
    return statically_known_true(sym_eq(arg.shape, tuple(size)))

