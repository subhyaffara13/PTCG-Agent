
def _nan_reduction(a: ArrayLike, name: str, jnp_reduction: Callable[..., Array],
                   init_val: ArrayLike, nan_if_all_nan: bool,
                   axis: Axis = None, keepdims: bool = False, where: ArrayLike | None = None,
                   **kwargs) -> Array:
  a = ensure_arraylike(name, a)
  where = check_where(name, where)
  if not dtypes.issubdtype(a.dtype, np.inexact):
    return jnp_reduction(a, axis=axis, keepdims=keepdims, where=where, **kwargs)

  out = jnp_reduction(_where(lax._isnan(a), _reduction_init_val(a, init_val), a),
                      axis=axis, keepdims=keepdims, where=where, **kwargs)
  if nan_if_all_nan:
    return _where(all(lax._isnan(a), axis=axis, keepdims=keepdims),
                  lax._const(a, np.nan), out)
  else:
    return out

