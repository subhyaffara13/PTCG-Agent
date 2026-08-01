
def method_registration(f: NativeFunction) -> str:
    if cpp.name(f.func) in MANUAL_TRACER:
        raise AssertionError(f"Function {cpp.name(f.func)} is in MANUAL_TRACER")

    return WRAPPER_REGISTRATION.substitute(
        name=f.func.name,
        type_wrapper_name=type_wrapper_name(f),
        class_type="TraceType",
    )

