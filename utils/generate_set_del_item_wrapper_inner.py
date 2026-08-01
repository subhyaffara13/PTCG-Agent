
def generate_set_del_item_wrapper_inner(
    fn: FuncIR, emitter: Emitter, args: Sequence[RuntimeArg]
) -> None:
    for arg in args:
        generate_arg_check(arg.name, arg.type, emitter, GotoHandler("fail"))
    native_args = ", ".join(f"arg_{arg.name}" for arg in args)
    emitter.emit_line(
        "{}val = {}({});".format(
            emitter.ctype_spaced(fn.ret_type), emitter.native_function_call(fn.decl), native_args
        )
    )
    emitter.emit_error_check("val", fn.ret_type, "goto fail;")
    emitter.emit_dec_ref("val", fn.ret_type)
    emitter.emit_line("return 0;")
    emitter.emit_label("fail")
    emitter.emit_line("return -1;")
    emitter.emit_line("}")

