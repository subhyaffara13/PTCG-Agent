
def generate_init_for_class(cl: ClassIR, init_fn: FuncIR, emitter: Emitter) -> str:
    """Generate an init function suitable for use as tp_init.

    tp_init needs to be a function that returns an int, and our
    __init__ methods return a PyObject. Translate NULL to -1,
    everything else to 0.
    """
    func_name = f"{cl.name_prefix(emitter.names)}_init"

    emitter.emit_line("static int")
    emitter.emit_line(f"{func_name}(PyObject *self, PyObject *args, PyObject *kwds)")
    emitter.emit_line("{")
    if cl.allow_interpreted_subclasses or cl.builtin_base or cl.has_method("__new__"):
        emitter.emit_line(
            f"return {emitter.wrapper_function_call(init_fn.decl)}"
            "(self, args, kwds) != NULL ? 0 : -1;"
        )
    else:
        emitter.emit_line("return 0;")
    emitter.emit_line("}")

    return func_name

