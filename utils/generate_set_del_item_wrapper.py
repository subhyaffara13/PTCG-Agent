
def generate_set_del_item_wrapper(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    """Generates a wrapper for native __setitem__ method (also works for __delitem__).

    This is used with the mapping protocol slot. Arguments are taken as *PyObjects and we
    return a negative C int on error.

    Create a separate wrapper function for __delitem__ as needed and have the
    __setitem__ wrapper call it if the value is NULL. Return the name
    of the outer (__setitem__) wrapper.
    """
    method_cls = cl.get_method_and_class("__delitem__")
    del_name = None
    if method_cls and method_cls[1] == cl:
        # Generate a separate wrapper for __delitem__
        del_name = generate_del_item_wrapper(cl, method_cls[0], emitter)

    args = fn.args
    if fn.name == "__delitem__":
        # Add an extra argument for value that we expect to be NULL.
        args = list(args) + [RuntimeArg("___value", object_rprimitive, ARG_POS)]

    name = "{}{}{}".format(DUNDER_PREFIX, "__setitem__", cl.name_prefix(emitter.names))
    input_args = ", ".join(f"PyObject *obj_{arg.name}" for arg in args)
    emitter.emit_line(f"static int {name}({input_args}) {{")

    # First check if this is __delitem__
    emitter.emit_line(f"if (obj_{args[2].name} == NULL) {{")
    if del_name is not None:
        # We have a native implementation, so call it
        emitter.emit_line(f"return {del_name}(obj_{args[0].name}, obj_{args[1].name});")
    else:
        # Try to call superclass method instead
        emitter.emit_line(f"PyObject *super = CPy_Super(CPyModule_builtins, obj_{args[0].name});")
        emitter.emit_line("if (super == NULL) return -1;")
        emitter.emit_line(
            'PyObject *result = PyObject_CallMethod(super, "__delitem__", "O", obj_{});'.format(
                args[1].name
            )
        )
        emitter.emit_line("Py_DECREF(super);")
        emitter.emit_line("Py_XDECREF(result);")
        emitter.emit_line("return result == NULL ? -1 : 0;")
    emitter.emit_line("}")

    method_cls = cl.get_method_and_class("__setitem__")
    if method_cls and method_cls[1] == cl:
        generate_set_del_item_wrapper_inner(fn, emitter, args)
    else:
        emitter.emit_line(f"PyObject *super = CPy_Super(CPyModule_builtins, obj_{args[0].name});")
        emitter.emit_line("if (super == NULL) return -1;")
        emitter.emit_line("PyObject *result;")

        if method_cls is None and cl.builtin_base is None:
            msg = f"'{cl.name}' object does not support item assignment"
            emitter.emit_line(f'PyErr_SetString(PyExc_TypeError, "{msg}");')
            emitter.emit_line("result = NULL;")
        else:
            # A base class may have __setitem__
            emitter.emit_line(
                'result = PyObject_CallMethod(super, "__setitem__", "OO", obj_{}, obj_{});'.format(
                    args[1].name, args[2].name
                )
            )
        emitter.emit_line("Py_DECREF(super);")
        emitter.emit_line("Py_XDECREF(result);")
        emitter.emit_line("return result == NULL ? -1 : 0;")
        emitter.emit_line("}")
    return name

