
def generate_get_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __get__ methods."""
    name = f"{DUNDER_PREFIX}{fn.name}{cl.name_prefix(emitter.names)}"
    emitter.emit_line(
        "static PyObject *{name}(PyObject *self, PyObject *instance, PyObject *owner) {{".format(
            name=name
        )
    )
    emitter.emit_line("instance = instance ? instance : Py_None;")
    emitter.emit_line(f"return {emitter.native_function_call(fn.decl)}(self, instance, owner);")
    emitter.emit_line("}")

    return name

