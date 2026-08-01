
def generate_finalize_for_class(
    del_method: FuncIR, finalize_func_name: str, emitter: Emitter
) -> None:
    emitter.emit_line("static void")
    emitter.emit_line(f"{finalize_func_name}(PyObject *self)")
    emitter.emit_line("{")
    emitter.emit_line(
        "{}{}{}(self);".format(
            emitter.get_group_prefix(del_method.decl),
            NATIVE_PREFIX,
            del_method.cname(emitter.names),
        )
    )
    emitter.emit_line("}")

