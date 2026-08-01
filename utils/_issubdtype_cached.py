
def _issubdtype_cached(a: type | np.dtype | ExtendedDType,
                       b: type | np.dtype | ExtendedDType) -> bool:
  # First handle extended dtypes, which require their own logic.
  a_is_type = isinstance(a, type)
  b_is_type = isinstance(b, type)
  if b_is_type and _issubclass(b, extended):
    if isinstance(a, ExtendedDType):
      return _issubclass(a.type, b)
    if a_is_type and _issubclass(a, np.generic):
      return _issubclass(a, b)
    return _issubclass(np.dtype(a).type, b)
  if isinstance(b, ExtendedDType):
    return isinstance(a, ExtendedDType) and a == b
  if isinstance(a, ExtendedDType):
    a = a.type
    a_is_type = isinstance(a, type)

  # For all others, normalize inputs to scalar types.
  a_sctype = a if a_is_type and _issubclass(a, np.generic) else np.dtype(a).type
  b_sctype = b if b_is_type and _issubclass(b, np.generic) else np.dtype(b).type

  # Now do special handling of custom float and int types, as they don't conform
  # to the normal scalar type hierarchy.
  if a_sctype in _custom_float_scalar_types:
    return b_sctype in {a_sctype, np.floating, np.inexact, np.number, np.generic}
  if a_sctype in [int2, int4] or (int1 is not None and a_sctype == int1):
    return b_sctype in {a_sctype, np.signedinteger, np.integer, np.number, np.generic}
  if a_sctype in [uint2, uint4] or (uint1 is not None and a_sctype == uint1):
    return b_sctype in {a_sctype, np.unsignedinteger, np.integer, np.number, np.generic}

  # Otherwise, fall back to numpy.issubdtype
  return bool(np.issubdtype(a_sctype, b_sctype))

