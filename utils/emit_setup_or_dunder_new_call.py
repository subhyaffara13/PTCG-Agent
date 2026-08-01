
def emit_setup_or_dunder_new_call(
    cl: ClassIR,
    setup_name: str,
    type_arg: str,
    native_prefix: bool,
    new_args: str,
    emitter: Emitter,
) -> None:
    def emit_null_check() -> None:
        emitter.emit_line("if (self == NULL)")
        emitter.emit_line("    return NULL;")

    new_fn = cl.get_method("__new__")
    if not new_fn:
        emitter.emit_line(f"PyObject *self = {setup_name}({type_arg});")
        emit_null_check()
        return
    call = (
        emitter.native_function_call(new_fn.decl)
        if native_prefix
        else emitter.wrapper_function_call(new_fn.decl)
    )
    all_args = type_arg
    if new_args != "":
        all_args += ", " + new_args
    emitter.emit_line(f"PyObject *self = {call}({all_args});")
    emit_null_check()

    # skip __init__ if __new__ returns some other type
    emitter.emit_line(f"if (Py_TYPE(self) != {emitter.type_struct_name(cl)})")
    emitter.emit_line("    return self;")

