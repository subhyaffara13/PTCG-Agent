
def generate_del_item_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __delitem__.

    This is only called from a combined __delitem__/__setitem__ wrapper.
    """
    name = "{}{}{}".format(DUNDER_PREFIX, "__delitem__", cl.name_prefix(emitter.names))
    input_args = ", ".join(f"PyObject *obj_{arg.name}" for arg in fn.args)
    emitter.emit_line(f"static int {name}({input_args}) {{")
    generate_set_del_item_wrapper_inner(fn, emitter, fn.args)
    return name

