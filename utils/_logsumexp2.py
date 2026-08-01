
def _logsumexp2(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
                out: None = None, keepdims: bool = False,
                initial: ArrayLike | None = None, where: ArrayLike | None = None) -> Array:
  """Compute log2(sum(2 ** a)) via logsumexp."""
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.logaddexp2.reduce is not supported.")
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(
        dtype, "jnp.logaddexp2.reduce")
  a = ensure_arraylike("logsumexp2", a)
  where = check_where("logsumexp2", where)
  ln2 = float(np.log(2))
  if initial is not None:
    initial *= ln2
  return _logsumexp(a * ln2, axis=axis, dtype=dtype, keepdims=keepdims,
                    where=where, initial=initial) / ln2

