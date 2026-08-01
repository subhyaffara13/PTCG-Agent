
def generate_bin_op_reverse_only_wrapper(
    fn: FuncIR, emitter: Emitter, gen: WrapperGenerator
) -> None:
    gen.arg_names = ["right", "left"]
    gen.emit_arg_processing(error=GotoHandler("typefail"), raise_exception=False)
    handle_third_pow_argument(fn, emitter, gen, if_unsupported=["goto typefail;"])
    gen.emit_call()
    gen.emit_error_handling()
    emitter.emit_label("typefail")
    emitter.emit_line("Py_INCREF(Py_NotImplemented);")
    emitter.emit_line("return Py_NotImplemented;")
    gen.finish()

