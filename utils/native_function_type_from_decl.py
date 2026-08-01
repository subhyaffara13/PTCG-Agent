
def native_function_type_from_decl(decl: FuncDecl, emitter: Emitter) -> str:
    args = ", ".join(emitter.ctype(arg.type) for arg in decl.sig.args) or "void"
    ret = emitter.ctype(decl.sig.ret_type)
    return f"{ret} (*)({args})"

