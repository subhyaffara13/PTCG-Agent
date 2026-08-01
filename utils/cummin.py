
def cummin(x, axis=None):
    if len(x.get_size()) == 0:
        assert axis in [0, -1]
        return clone(x), empty_like(x, dtype=torch.int64)

    dtype = x.get_dtype()
    combine_fn = ir.get_reduction_combine_fn(
        "argmin", dtype=dtype, arg_break_ties_left=False
    )

    kwargs = _make_scan_inner(x, axis=axis, dtype=dtype)
    kwargs["dtypes"] = (dtype, torch.int64)
    kwargs["inner_fns"] = (
        x.make_loader(),
        lambda idx: ops.index_expr(idx[axis], torch.int64),
    )
    values, indices = ir.Scan.create(**kwargs, combine_fn=combine_fn)  # type: ignore[arg-type]
    if values is None:
        return fallback_cummin(x, dim=axis)
    return values, indices


def cummin(whatever):
    pass


def cummin(values: np.ndarray, *, skipna: bool = True) -> np.ndarray:
    return _cum_func(np.minimum.accumulate, values, skipna=skipna)


def cummin(
    values: np.ndarray, mask: npt.NDArray[np.bool_], *, skipna: bool = True
) -> tuple[np.ndarray, npt.NDArray[np.bool_]]:
    return _cum_func(np.minimum.accumulate, values, mask, skipna=skipna)


def cummin(x: jax.Array, *, mask: jax.Array | None = None) -> jax.Array:
  """Returns the cumulative min of the array along its innermost axis.

  Elements from `x` will pass through directly to the result until the first
  valid value is encountered (`mask[i] == True`). If you would like to specify
  a default value for such elements instead, write
  `x = jnp.where(mask, x, default_value)` before or after calling this function.

  Args:
    x: An array of integers or floats.
    mask: An optional array of booleans, which specifies which elements of `x`
      are eligible for the min. If `None`, all elements are eligible.
  """
  if x.ndim != 1:
    raise NotImplementedError(f"cummin: x={x.aval} must be rank 1")
  if mask is None:
    mask = lax.full(x.shape, True)
  return masked_cummin_p.bind(x, mask)


def cummin(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative minimum along `axis`."""
  return cummin_p.bind(operand, axis=int(axis), reverse=bool(reverse))

