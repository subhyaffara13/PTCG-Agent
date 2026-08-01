
def generate_coroutine_setup(
    cl: ClassIR, coroutine_setup_name: str, module_name: str, emitter: Emitter
) -> None:
    emitter.emit_line("static bool")
    emitter.emit_line(f"{NATIVE_PREFIX}{coroutine_setup_name}(PyObject *type)")
    emitter.emit_line("{")

    error_stmt = "    return 2;"

    def emit_instance(fn: FuncIR, fn_name: str) -> str:
        filepath = emitter.filepath or ""
        return emitter.emit_cpyfunction_instance(fn, fn_name, filepath, error_stmt)

    def success() -> None:
        emitter.emit_line("return 1;")
        emitter.emit_line("}")

    if cl.coroutine_name:
        # Callable class generated for a coroutine. It stores its function wrapper as an attribute.
        wrapper_name = emit_instance(cl.methods["__call__"], cl.coroutine_name)
        struct_name = cl.struct_name(emitter.names)
        attr = emitter.attr(CPYFUNCTION_NAME)
        emitter.emit_line(f"(({struct_name} *)type)->{attr} = {wrapper_name};")
        return success()

    if not any(fn.decl.is_coroutine for fn in cl.methods.values()):
        return success()

    emitter.emit_line("PyTypeObject *tp = (PyTypeObject *)type;")

    for fn in cl.methods.values():
        if not fn.decl.is_coroutine:
            continue

        name = short_id_from_name(fn.name, fn.decl.shortname, fn.line)
        wrapper_name = emit_instance(fn, name)
        name_obj = f"{wrapper_name}_name"
        emitter.emit_line(f'PyObject *{name_obj} = PyUnicode_FromString("{fn.name}");')
        emitter.emit_line(f"if (unlikely(!{name_obj}))")
        emitter.emit_line(error_stmt)
        emitter.emit_line(f"if (PyDict_SetItem(tp->tp_dict, {name_obj}, {wrapper_name}) < 0)")
        emitter.emit_line(error_stmt)

    return success()

