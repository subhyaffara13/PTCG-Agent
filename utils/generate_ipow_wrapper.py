
def generate_ipow_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generate a wrapper for native __ipow__.

    Since __ipow__ fills a ternary slot, but almost no one defines __ipow__ to take three
    arguments, the wrapper needs to tweaked to force it to accept three arguments.
    """
    gen = WrapperGenerator(cl, emitter)
    gen.set_target(fn)
    assert len(fn.args) in (2, 3), "__ipow__ should only take 2 or 3 arguments"
    gen.arg_names = ["self", "exp", "mod"]
    gen.emit_header()
    gen.emit_arg_processing()
    handle_third_pow_argument(
        fn,
        emitter,
        gen,
        if_unsupported=[
            'PyErr_SetString(PyExc_TypeError, "__ipow__ takes 2 positional arguments but 3 were given");',
            "return NULL;",
        ],
    )
    gen.emit_call()
    gen.finish()
    return gen.wrapper_name()

