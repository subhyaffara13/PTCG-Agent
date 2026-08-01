
def generate_bin_op_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for a native binary dunder method.

    The same wrapper that handles the forward method (e.g. __add__) also handles
    the corresponding reverse method (e.g. __radd__), if defined.

    Both arguments and the return value are PyObject *.
    """
    gen = WrapperGenerator(cl, emitter)
    gen.set_target(fn)
    if fn.name in ("__pow__", "__rpow__"):
        gen.arg_names = ["left", "right", "mod"]
    else:
        gen.arg_names = ["left", "right"]
    wrapper_name = gen.wrapper_name()

    gen.emit_header()
    if fn.name not in reverse_op_methods and fn.name in reverse_op_method_names:
        # There's only a reverse operator method.
        generate_bin_op_reverse_only_wrapper(fn, emitter, gen)
    else:
        rmethod = reverse_op_methods[fn.name]
        fn_rev = cl.get_method(rmethod)
        if fn_rev is None:
            # There's only a forward operator method.
            generate_bin_op_forward_only_wrapper(fn, emitter, gen)
        else:
            # There's both a forward and a reverse operator method.
            generate_bin_op_both_wrappers(cl, fn, fn_rev, emitter, gen)
    return wrapper_name

