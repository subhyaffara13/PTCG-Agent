
def generate_new_for_class(
    cl: ClassIR,
    func_name: str,
    vtable_name: str,
    setup_name: str,
    init_fn: FuncIR | None,
    emitter: Emitter,
) -> None:
    emitter.emit_line("static PyObject *")
    emitter.emit_line(f"{func_name}(PyTypeObject *type, PyObject *args, PyObject *kwds)")
    emitter.emit_line("{")
    # TODO: Check and unbox arguments
    if not cl.allow_interpreted_subclasses:
        emitter.emit_line(f"if (type != {emitter.type_struct_name(cl)}) {{")
        emitter.emit_line(
            'PyErr_SetString(PyExc_TypeError, "interpreted classes cannot inherit from compiled");'
        )
        emitter.emit_line("return NULL;")
        emitter.emit_line("}")

    type_arg = "(PyObject*)type"
    new_args = "args, kwds"
    emit_setup_or_dunder_new_call(cl, setup_name, type_arg, False, new_args, emitter)
    if (
        not init_fn
        or cl.allow_interpreted_subclasses
        or cl.builtin_base
        or cl.is_serializable()
        or cl.has_method("__new__")
    ):
        # Match Python semantics -- __new__ doesn't call __init__.
        emitter.emit_line("return self;")
    else:
        # __new__ of a native class implicitly calls __init__ so that we
        # can enforce that instances are always properly initialized. This
        # is needed to support always defined attributes.
        emitter.emit_line(
            f"PyObject *ret = {emitter.wrapper_function_call(init_fn.decl)}(self, args, kwds);"
        )
        emitter.emit_lines("if (ret == NULL) {", "    Py_DECREF(self);", "    return NULL;", "}")
        emitter.emit_line("Py_DECREF(ret);")
        emitter.emit_line("return self;")
    emitter.emit_line("}")

