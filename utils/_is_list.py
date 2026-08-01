
def _is_list(x: _C.Value) -> bool:
    return _as_list_type(x.type()) is not None

