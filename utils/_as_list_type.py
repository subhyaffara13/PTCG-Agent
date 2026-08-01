
def _as_list_type(jit_type: _C.JitType) -> _C.ListType | None:
    if isinstance(jit_type, _C.ListType):
        return jit_type
    return None

