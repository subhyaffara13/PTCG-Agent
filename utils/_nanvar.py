
def _nanvar(a: Array, *, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None, a_mean: ArrayLike | None = None) -> Array:
  computation_dtype, dtype = _var_promote_types(a.dtype, dtype)
  a = lax.asarray(a).astype(computation_dtype)
  if a_mean is None:
    a_mean = nanmean(a, axis, dtype=computation_dtype, keepdims=True, where=where)
  else:
    a_mean = ensure_arraylike("nanvar", a_mean).astype(computation_dtype)

  centered = _where(lax._isnan(a), 0, lax.sub(a, a_mean))  # double-where trick for gradients.
  if dtypes.issubdtype(centered.dtype, np.complexfloating):
    centered = lax.real(lax.mul(centered, lax.conj(centered)))
  else:
    centered = lax.square(centered)

  normalizer = sum(lax.bitwise_not(lax._isnan(a)),
                   axis=axis, keepdims=keepdims, where=where)
  normalizer = normalizer - ddof
  normalizer_mask = lax.le(normalizer, lax._zero(normalizer))
  result = sum(centered, axis, keepdims=keepdims, where=where)
  result = _where(normalizer_mask, np.nan, result)
  divisor = _where(normalizer_mask, 1, normalizer)
  result = lax.div(result, lax.convert_element_type(divisor, result.dtype))
  return lax.convert_element_type(result, dtype)

