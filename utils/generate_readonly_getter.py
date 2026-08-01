
def generate_readonly_getter(
    cl: ClassIR, attr: str, rtype: RType, func_ir: FuncIR, emitter: Emitter
) -> None:
    emitter.emit_line("static PyObject *")
    emitter.emit_line(
        "{}({} *self, void *closure)".format(
            getter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
        )
    )
    emitter.emit_line("{")
    if rtype.is_unboxed:
        emitter.emit_line(
            "{}retval = {}{}((PyObject *) self);".format(
                emitter.ctype_spaced(rtype), NATIVE_PREFIX, func_ir.cname(emitter.names)
            )
        )
        emitter.emit_error_check("retval", rtype, "return NULL;")
        emitter.emit_box("retval", "retbox", rtype, declare_dest=True)
        emitter.emit_line("return retbox;")
    else:
        emitter.emit_line(
            f"return {NATIVE_PREFIX}{func_ir.cname(emitter.names)}((PyObject *) self);"
        )
    emitter.emit_line("}")

