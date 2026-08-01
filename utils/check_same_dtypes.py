
def check_same_dtypes(name: str, *avals: ShapedArray) -> None:
  """Check that dtypes agree, possibly ignoring float precision."""
  # the `ignore_fp_precision` flag exists because the XLA shape inference logic
  # allows mixed floating point precision, but the HLO verifier often rejects it
  if any(dtypes.issubdtype(aval.dtype, dtypes.extended) for aval in avals):
    return  # TODO(mattjj,frostig): do some checking, friend
  if len(avals) < 2:
    return

  dtype = avals[0].dtype
  if any(aval.dtype != dtype for aval in avals[1:]):
    msg = "lax.{} requires arguments to have the same dtypes, got {}."
    if name in _JNP_FUNCTION_EQUIVALENTS:
      equiv = _JNP_FUNCTION_EQUIVALENTS[name]
      msg += f" (Tip: jnp.{equiv} is a similar function that does automatic type promotion on inputs)."
    raise TypeError(msg.format(name, ", ".join(str(a.dtype) for a in avals)))

