
def generate_methods_table(
    cl: ClassIR, name: str, setup_name: str | None, emitter: Emitter
) -> None:
    emitter.emit_line(f"static PyMethodDef {name}[] = {{")
    if setup_name:
        # Store pointer to the setup function so it can be resolved dynamically
        # in case of instance creation in __new__.
        # CPy_SetupObject expects this method to be the first one in tp_methods.
        emitter.emit_line(
            f'{{"__internal_mypyc_setup", (PyCFunction){setup_name}, METH_O, NULL}},'
        )
    for fn in cl.methods.values():
        if fn.decl.is_prop_setter or fn.decl.is_prop_getter or fn.internal:
            continue
        emitter.emit_line(f'{{"{fn.name}",')
        emitter.emit_line(f" (PyCFunction){PREFIX}{fn.cname(emitter.names)},")
        flags = ["METH_FASTCALL", "METH_KEYWORDS"]
        if fn.decl.kind == FUNC_STATICMETHOD:
            flags.append("METH_STATIC")
        elif fn.decl.kind == FUNC_CLASSMETHOD:
            flags.append("METH_CLASS")

        doc = native_function_doc_initializer(fn)
        emitter.emit_line(" {}, PyDoc_STR({})}},".format(" | ".join(flags), doc))

    # Provide a default __getstate__ and __setstate__
    if not cl.has_method("__setstate__") and not cl.has_method("__getstate__"):
        emitter.emit_lines(
            '{"__setstate__", (PyCFunction)CPyPickle_SetState, METH_O, NULL},',
            '{"__getstate__", (PyCFunction)CPyPickle_GetState, METH_NOARGS, NULL},',
        )

    emitter.emit_line("{NULL}  /* Sentinel */")
    emitter.emit_line("};")

