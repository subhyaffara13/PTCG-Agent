
def _to_bool(s: bytes) -> bool:
    if s.lower().strip() in (b'false', b'0', b'no'):
        return False
    else:
        return True


def _to_bool(v: str) -> bool:
    return v in ("1", "true")


def _to_bool(x: Array) -> Array:
  return x if x.dtype == bool else lax.ne(x, _lax_const(x, 0))

