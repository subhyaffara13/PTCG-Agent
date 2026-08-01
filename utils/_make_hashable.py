
def _make_hashable(val):
  if isinstance(val, (core.Jaxpr, core.ClosedJaxpr)):
    return _jaxpr_signature(val)
  elif isinstance(val, (list, tuple)):
    return tuple(_make_hashable(v) for v in val)
  elif isinstance(val, dict):
    return tuple(sorted((k, _make_hashable(v)) for k, v in val.items()))
  elif isinstance(val, (set, frozenset)):
    return frozenset(_make_hashable(v) for v in val)
  elif hasattr(val, 'shape') and hasattr(val, 'dtype'):
    try:
      b = (
          val.tobytes()
          if hasattr(val, 'tobytes')
          else np.asarray(val).tobytes()
      )
      arr_hash = hashlib.sha256(b).hexdigest()
      return ('array', tuple(val.shape), str(val.dtype), arr_hash)
    except Exception:
      return ('array_fallback', tuple(val.shape), str(val.dtype))
  else:
    try:
      hash(val)
      return type(val), val
    except TypeError:
      return type(val), str(val)

