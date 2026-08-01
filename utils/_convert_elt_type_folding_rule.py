
def _convert_elt_type_folding_rule(consts, params, out_avals):
  # We constant-fold convert_element_types applied to constants if those
  # constants are Python builtin numeric types or numpy.ndarrays (so as not
  # to perform any device operations when constant-folding) and if the output
  # type can be faithfully represented by a Python builtin numeric type or
  # numpy.ndarray. If those conditions are met, we output a numpy.ndarray
  # constant if the output type is not weak, and if the output type is weak then
  # we output a Python builtin numeric type.
  # TODO(mattjj): allow constant-folding CPU-backed JAX arrays
  c, = consts
  out_aval, = out_avals
  new_dtype = params['new_dtype']
  if (type(c) in _foldable_types and isinstance(out_aval, ShapedArray)
      and not np.shape(c)
      and not dtypes.issubdtype(new_dtype, dtypes.extended)):
    out = np.asarray(c)
    if (dtypes.issubdtype(out.dtype, np.complexfloating) and
        not dtypes.issubdtype(new_dtype, np.complexfloating)):
      out = out.real
    out = out.astype(new_dtype)
    return [literals.TypedNdArray(out, aval=out_aval)]
  return None

