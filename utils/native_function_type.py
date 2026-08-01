
def native_function_type(fn: FuncIR, emitter: Emitter) -> str:
    return native_function_type_from_decl(fn.decl, emitter)

