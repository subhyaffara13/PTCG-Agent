
def generate_property_setter(
    cl: ClassIR, attr: str, arg_type: RType, func_ir: FuncIR, emitter: Emitter
) -> None:
    emitter.emit_line("static int")
    emitter.emit_line(
        "{}({} *self, PyObject *value, void *closure)".format(
            setter_name(cl, attr, emitter.names), cl.struct_name(emitter.names)
        )
    )
    emitter.emit_line("{")
    if arg_type.is_unboxed:
        emitter.emit_unbox("value", "tmp", arg_type, error=ReturnHandler("-1"), declare_dest=True)
        emitter.emit_line(
            f"{NATIVE_PREFIX}{func_ir.cname(emitter.names)}((PyObject *) self, tmp);"
        )
    else:
        emitter.emit_line(
            f"{NATIVE_PREFIX}{func_ir.cname(emitter.names)}((PyObject *) self, value);"
        )
    emitter.emit_line("return 0;")
    emitter.emit_line("}")

