
def generate_dunder_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __dunder__ methods to be able to fit into the mapping
    protocol slot. This specifically means that the arguments are taken as *PyObjects and returned
    as *PyObjects.
    """
    gen = WrapperGenerator(cl, emitter)
    gen.set_target(fn)
    gen.emit_header()
    gen.emit_arg_processing()
    gen.emit_call()
    gen.finish()
    return gen.wrapper_name()

