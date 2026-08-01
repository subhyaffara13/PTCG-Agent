
def is_fastcall_supported(fn: FuncIR, capi_version: tuple[int, int]) -> bool:
    if fn.class_name is not None:
        if fn.name == "__call__":
            # We can use vectorcalls (PEP 590) when supported
            return True
        # TODO: Support fastcall for __init__ and __new__.
        return fn.name != "__init__" and fn.name != "__new__"
    return True

