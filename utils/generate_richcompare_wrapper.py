
def generate_richcompare_wrapper(cl: ClassIR, emitter: Emitter) -> str | None:
    """Generates a wrapper for richcompare dunder methods."""
    # Sort for determinism on Python 3.5
    matches = sorted(name for name in RICHCOMPARE_OPS if cl.has_method(name))
    if not matches:
        return None

    name = f"{DUNDER_PREFIX}_RichCompare_{cl.name_prefix(emitter.names)}"
    emitter.emit_line(
        "static PyObject *{name}(PyObject *obj_lhs, PyObject *obj_rhs, int op) {{".format(
            name=name
        )
    )
    emitter.emit_line("switch (op) {")
    for func in matches:
        emitter.emit_line(f"case {RICHCOMPARE_OPS[func]}: {{")
        method = cl.get_method(func)
        assert method is not None
        generate_wrapper_core(method, emitter, arg_names=["lhs", "rhs"])
        emitter.emit_line("}")
    emitter.emit_line("}")

    emitter.emit_line("Py_INCREF(Py_NotImplemented);")
    emitter.emit_line("return Py_NotImplemented;")

    emitter.emit_line("}")

    return name

