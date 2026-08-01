
def native_slot(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    return f"{NATIVE_PREFIX}{fn.cname(emitter.names)}"

