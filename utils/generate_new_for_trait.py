
def generate_new_for_trait(cl: ClassIR, func_name: str, emitter: Emitter) -> None:
    emitter.emit_line("static PyObject *")
    emitter.emit_line(f"{func_name}(PyTypeObject *type, PyObject *args, PyObject *kwds)")
    emitter.emit_line("{")
    emitter.emit_line(f"if (type != {emitter.type_struct_name(cl)}) {{")
    emitter.emit_line(
        "PyErr_SetString(PyExc_TypeError, "
        '"interpreted classes cannot inherit from compiled traits");'
    )
    emitter.emit_line("} else {")
    emitter.emit_line('PyErr_SetString(PyExc_TypeError, "traits may not be directly created");')
    emitter.emit_line("}")
    emitter.emit_line("return NULL;")
    emitter.emit_line("}")

