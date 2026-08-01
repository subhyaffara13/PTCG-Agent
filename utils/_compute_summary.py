
def _compute_summary(
    x: jax.Array, is_floating: bool, is_integer: bool, is_bool: bool, xnp=None
) -> dict[str, jax.Array]:
  """Computes a summary of the given array."""
  if xnp is None:
    assert jax is not None, "JAX is not available."
    xnp = jax.numpy
  x = xnp.array(x)
  result = {}
  if is_floating:
    isfinite = xnp.isfinite(x)
    inf_to_nan = xnp.where(isfinite, x, xnp.array(xnp.nan, dtype=x.dtype))
    nanmean = functools.partial(xnp.nanmean, dtype=xnp.float32)
    nanstd = functools.partial(xnp.nanstd, dtype=xnp.float32)
    nanmin = lambda x: xnp.nanmin(x).astype(xnp.float32)
    nanmax = lambda x: xnp.nanmax(x).astype(xnp.float32)
    result.update(mean=nanmean(inf_to_nan), std=nanstd(inf_to_nan))
    result.update(nanmin=nanmin(x), nanmax=nanmax(x))
    result.update(
        nan=xnp.count_nonzero(xnp.isnan(x)),
        inf=xnp.count_nonzero(xnp.isposinf(x)),
    )
    result["any_finite"] = xnp.any(isfinite)
    result["-inf"] = xnp.count_nonzero(xnp.isneginf(x))
  if is_integer:
    result.update(min=xnp.min(x), max=xnp.max(x))
  if is_floating or is_integer:
    result.update(zero=xnp.count_nonzero(x == 0), nonzero=xnp.count_nonzero(x))
  if is_bool:
    result.update(
        true=xnp.count_nonzero(x), false=xnp.count_nonzero(xnp.logical_not(x))
    )
  return result

