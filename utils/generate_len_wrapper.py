
def generate_len_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __len__ methods."""
    name = f"{DUNDER_PREFIX}{fn.name}{cl.name_prefix(emitter.names)}"
    emitter.emit_line(f"static Py_ssize_t {name}(PyObject *self) {{")
    emitter.emit_line(
        "{}retval = {}{}{}(self);".format(
            emitter.ctype_spaced(fn.ret_type),
            emitter.get_group_prefix(fn.decl),
            NATIVE_PREFIX,
            fn.cname(emitter.names),
        )
    )
    emitter.emit_error_check("retval", fn.ret_type, "return -1;")
    if is_int_rprimitive(fn.ret_type):
        emitter.emit_line("Py_ssize_t val = CPyTagged_AsSsize_t(retval);")
    else:
        emitter.emit_line("Py_ssize_t val = PyLong_AsSsize_t(retval);")
    emitter.emit_dec_ref("retval", fn.ret_type)
    emitter.emit_line("if (PyErr_Occurred()) return -1;")
    emitter.emit_line("return val;")
    emitter.emit_line("}")

    return name

