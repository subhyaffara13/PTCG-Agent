
def _check_input_dtype_revderiv(name, holomorphic, allow_int, x):
  dispatch.check_arg(x)
  aval = core.typeof(x)
  if holomorphic:
    if not dtypes.issubdtype(aval.dtype, np.complexfloating):
      raise TypeError(f"{name} with holomorphic=True requires inputs with complex dtype, "
                      f"but got {aval.dtype.name}.")
  if isinstance(aval, ShapedArray):
    if (dtypes.issubdtype(aval.dtype, dtypes.extended) or
        dtypes.issubdtype(aval.dtype, np.integer) or
        dtypes.issubdtype(aval.dtype, np.bool_)):
      if not allow_int:
        raise TypeError(f"{name} requires real- or complex-valued inputs (input dtype "
                        f"that is a sub-dtype of np.inexact), but got {aval.dtype.name}. "
                        "If you want to use Boolean- or integer-valued inputs, use vjp "
                        "or set allow_int to True.")
    elif not dtypes.issubdtype(aval.dtype, np.inexact):
      raise TypeError(f"{name} requires numerical-valued inputs (input dtype that is a "
                      f"sub-dtype of np.bool_ or np.number), but got {aval.dtype.name}.")

