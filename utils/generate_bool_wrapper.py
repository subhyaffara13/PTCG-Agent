
def generate_bool_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __bool__ methods."""
    name = f"{DUNDER_PREFIX}{fn.name}{cl.name_prefix(emitter.names)}"
    emitter.emit_line(f"static int {name}(PyObject *self) {{")
    emitter.emit_line(
        "{}val = {}(self);".format(
            emitter.ctype_spaced(fn.ret_type), emitter.native_function_call(fn.decl)
        )
    )
    emitter.emit_error_check("val", fn.ret_type, "return -1;")
    # This wouldn't be that hard to fix but it seems unimportant and
    # getting error handling and unboxing right would be fiddly. (And
    # way easier to do in IR!)
    assert is_bool_rprimitive(fn.ret_type), "Only bool return supported for __bool__"
    emitter.emit_line("return val;")
    emitter.emit_line("}")

    return name

