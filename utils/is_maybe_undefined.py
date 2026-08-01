
def is_maybe_undefined(post_must_defined: set[Value], src: Value) -> bool:
    return (isinstance(src, Register) and src not in post_must_defined) or (
        isinstance(src, CallC) and src.returns_null
    )

