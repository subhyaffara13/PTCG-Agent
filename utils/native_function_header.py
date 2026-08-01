
def native_function_header(fn: FuncDecl, emitter: Emitter) -> str:
    args = []
    for arg in fn.sig.args:
        args.append(f"{emitter.ctype_spaced(arg.type)}{REG_PREFIX}{arg.name}")

    return "{ret_type}{name}({args})".format(
        ret_type=emitter.ctype_spaced(fn.sig.ret_type),
        name=emitter.native_function_name(fn),
        args=", ".join(args) or "void",
    )

