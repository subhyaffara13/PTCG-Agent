
def handle_third_pow_argument(
    fn: FuncIR, emitter: Emitter, gen: WrapperGenerator, *, if_unsupported: list[str]
) -> None:
    if fn.name not in ("__pow__", "__rpow__", "__ipow__"):
        return

    if (fn.name in ("__pow__", "__ipow__") and len(fn.args) == 2) or fn.name == "__rpow__":
        # If the power dunder only supports two arguments and the third
        # argument (AKA mod) is set to a non-default value, simply bail.
        #
        # Importantly, this prevents any ternary __rpow__ calls from
        # happening (as per the language specification).
        emitter.emit_line("if (obj_mod != Py_None) {")
        for line in if_unsupported:
            emitter.emit_line(line)
        emitter.emit_line("}")
        # The slot wrapper will receive three arguments, but the call only
        # supports two so make sure that the third argument isn't passed
        # along. This is needed as two-argument __(i)pow__ is allowed and
        # rather common.
        if len(gen.arg_names) == 3:
            gen.arg_names.pop()

