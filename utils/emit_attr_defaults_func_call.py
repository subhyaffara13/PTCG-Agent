
def emit_attr_defaults_func_call(defaults_fn: FuncIR, self_name: str, emitter: Emitter) -> None:
    """Emit C code to initialize attribute defaults by calling defaults_fn.

    The code returns NULL on a raised exception.
    """
    emitter.emit_lines(
        "if ({}((PyObject *){}) == 0) {{".format(
            emitter.native_function_call(defaults_fn.decl), self_name
        ),
        "Py_DECREF(self);",
        "return NULL;",
        "}",
    )

