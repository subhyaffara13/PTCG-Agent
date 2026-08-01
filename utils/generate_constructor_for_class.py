
def generate_constructor_for_class(
    cl: ClassIR,
    fn: FuncDecl,
    init_fn: FuncIR | None,
    setup_name: str,
    vtable_name: str,
    emitter: Emitter,
) -> None:
    """Generate a native function that allocates and initializes an instance of a class."""
    emitter.emit_line(f"{native_function_header(fn, emitter)}")
    emitter.emit_line("{")

    fn_args = [REG_PREFIX + arg.name for arg in fn.sig.args]
    type_arg = "(PyObject *)" + emitter.type_struct_name(cl)
    new_args = ", ".join(fn_args)

    use_wrapper = (
        cl.has_method("__new__")
        and len(fn.sig.args) == 2
        and fn.sig.args[0].kind == ARG_STAR
        and fn.sig.args[1].kind == ARG_STAR2
    )
    emit_setup_or_dunder_new_call(cl, setup_name, type_arg, not use_wrapper, new_args, emitter)

    args = ", ".join(["self"] + fn_args)
    if init_fn is not None:
        call = (
            emitter.wrapper_function_call(init_fn.decl)
            if use_wrapper
            else emitter.native_function_call(init_fn.decl)
        )
        cast = "!= NULL ? 0 : -1" if use_wrapper else ""
        emitter.emit_line(f"char res = {call}({args}){cast};")
        emitter.emit_line("if (res == 2) {")
        emitter.emit_line("Py_DECREF(self);")
        emitter.emit_line("return NULL;")
        emitter.emit_line("}")

    # If there is a nontrivial ctor that we didn't define, invoke it via tp_init
    elif len(fn.sig.args) > 1:
        emitter.emit_line(f"int res = {emitter.type_struct_name(cl)}->tp_init({args});")

        emitter.emit_line("if (res < 0) {")
        emitter.emit_line("Py_DECREF(self);")
        emitter.emit_line("return NULL;")
        emitter.emit_line("}")

    emitter.emit_line("return self;")
    emitter.emit_line("}")

