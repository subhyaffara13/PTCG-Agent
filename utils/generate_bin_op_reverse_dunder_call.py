
def generate_bin_op_reverse_dunder_call(fn: FuncIR, emitter: Emitter, rmethod: str) -> None:
    if fn.name in ("__pow__", "__rpow__"):
        # Ternary pow() will never call the reverse dunder.
        emitter.emit_line("if (obj_mod == Py_None) {")
    emitter.emit_line(
        'return CPy_CallReverseOpMethod(obj_left, obj_right, "{}", mypyc_interned_str.{});'.format(
            op_methods_to_symbols[fn.name], rmethod
        )
    )
    if fn.name in ("__pow__", "__rpow__"):
        emitter.emit_line("} else {")
        emitter.emit_line("Py_INCREF(Py_NotImplemented);")
        emitter.emit_line("return Py_NotImplemented;")
        emitter.emit_line("}")

