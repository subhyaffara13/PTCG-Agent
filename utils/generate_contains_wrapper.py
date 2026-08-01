
def generate_contains_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for a native __contains__ method."""
    name = f"{DUNDER_PREFIX}{fn.name}{cl.name_prefix(emitter.names)}"
    emitter.emit_line(f"static int {name}(PyObject *self, PyObject *obj_item) {{")
    generate_arg_check("item", fn.args[1].type, emitter, ReturnHandler("-1"))
    emitter.emit_line(
        "{}val = {}(self, arg_item);".format(
            emitter.ctype_spaced(fn.ret_type), emitter.native_function_call(fn.decl)
        )
    )
    emitter.emit_error_check("val", fn.ret_type, "return -1;")
    if is_bool_rprimitive(fn.ret_type):
        emitter.emit_line("return val;")
    else:
        emitter.emit_line("int boolval = PyObject_IsTrue(val);")
        emitter.emit_dec_ref("val", fn.ret_type)
        emitter.emit_line("return boolval;")
    emitter.emit_line("}")

    return name

