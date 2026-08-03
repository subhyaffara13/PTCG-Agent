from typing import Any

def _reshape(self: Array, *args: Any, order: str = "C", out_sharding=None
             ) -> Array:
  """Returns an array containing the same data with a new shape.

  Refer to :func:`jax.numpy.reshape` for full documentation.
  """
  __tracebackhide__ = True
  newshape = _compute_newshape(self, args[0] if len(args) == 1 else args)
  if order == "C":
    return lax.reshape(self, newshape, None, out_sharding=out_sharding)
  elif order == "F":
    dims = list(range(self.ndim)[::-1])
    out_sharding = canonicalize_sharding(out_sharding, "jnp.reshape")
    out_sharding = (
        None if out_sharding is None else out_sharding.update(
            spec=out_sharding.spec.update(partitions=out_sharding.spec[::-1])))
    return lax.reshape(self, newshape[::-1], dims, out_sharding=out_sharding).T
  elif order == "A":
    raise NotImplementedError("np.reshape order=A is not implemented.")
  else:
    raise ValueError(f"Unexpected value for 'order' argument: {order}.")


def _reshape(a: ir.Value, shape: Sequence[int]) -> ir.Value:
  if not isinstance(a.type, ir.RankedTensorType):
    assert all(dim_size == 1 for dim_size in shape)
    return _splat(a, shape)

  ty = ir.RankedTensorType(a.type)
  return tt_dialect.reshape(
      ir.RankedTensorType.get(shape, ty.element_type, ty.encoding),
      a,
      allow_reorder=False,
  )


def _reshape(self, *args, **kwargs):
  """Returns an array containing the same data with a new shape."""
  return sparsify(lambda x: x.reshape(*args, **kwargs))(self)


def _reshape(ref: ir.Value, sh0: list[int], sh1: list[int]):
  """Reshapes using only "parallel" folds/unfolds.

  This function uses folds/unfolds that are "parallel" in that they
  only act on original dimensions, i.e. they won't fold into an
  intermediate dimension that they will then unfold.
  """

  i0, i1 = 0, 0

  def fold_until(shape, off, target) -> tuple[int, int]:
    assert shape[off] < target
    dim = 1
    for to in range(off, len(shape)):
      dim *= shape[to]
      if dim == target:
        return to + 1, dim
      if dim > target:
        # TODO(cperivol): Implement dependent fold-unfolds for subsections
        # of the shape eg (..., 4,5,5, ...) -> (..., 10,10, ...) could be
        # supported without touching any other dimensions.
        raise NotImplementedError(
            f"Can't reshape {sh0} to {sh1} by composing independent"
            " folds/unfolds."
        )

    raise AssertionError(
        f"Unreachable: number of elements don't match in each shape ({sh0} ans"
        f" {sh1})"
    )

  while i0 < len(sh0) and i1 < len(sh1):
    if sh0[i0] > sh1[i1]:
      # How many dimensions following i1 should we unfold i0 into.
      idx, _ = fold_until(sh1, i1, sh0[i0])
      ref = memref_unfold(ref, i0, sh1[i1:idx])
      sh0[i0 : i0 + 1] = sh1[i1:idx]
      i0 += idx - i1
      i1 = idx
    elif sh0[i0] < sh1[i1]:
      # How many dimensions after i0 should we fold to make dim at i1.
      idx, dim = fold_until(sh0, i0, sh1[i1])
      sh0[i0:idx] = [dim]
      ref = memref_fold(ref, i0, idx - i0)
      i0 += 1
      i1 += 1
    else:
      i0 += 1
      i1 += 1

  # Fold the trailing ones
  if i0 < len(sh0):
    assert i1 == len(sh1)
    ref = memref_fold(ref, i0 - 1, len(sh0) - i0 + 1)

  if i1 < len(sh1):
    assert i0 == len(sh0)
    ref = memref_unfold(ref, i0 - 1, [sh0[i0 - 1]] + [1] * (len(sh1) - i1))

  return ref

