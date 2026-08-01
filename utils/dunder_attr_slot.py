
def dunder_attr_slot(cl: ClassIR, fn: FuncIR, emitter: Emitter) -> str:
    wrapper_fn = cl.get_method(fn.name + "__wrapper")
    assert wrapper_fn
    return f"{NATIVE_PREFIX}{wrapper_fn.cname(emitter.names)}"

