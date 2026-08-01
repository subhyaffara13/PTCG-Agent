
def scatter_mul(
  operand: ArrayLike, scatter_indices: ArrayLike, updates: ArrayLike,
  dimension_numbers: ScatterDimensionNumbers, *,
  indices_are_sorted: bool = False, unique_indices: bool = False,
  mode: str | GatherScatterMode | None = None) -> Array:
  """Scatter-multiply operator.

  Wraps `XLA's Scatter operator
  <https://www.openxla.org/xla/operation_semantics#scatter>`_, where
  multiplication is used to combine updates and values from `operand`.

  The semantics of scatter are complicated, and its API might change in the
  future. For most use cases, you should prefer the
  :attr:`jax.numpy.ndarray.at` property on JAX arrays which uses
  the familiar NumPy indexing syntax.

  Args:
    operand: an array to which the scatter should be applied
    scatter_indices: an array that gives the indices in `operand` to which each
      update in `updates` should be applied.
    updates: the updates that should be scattered onto `operand`.
    dimension_numbers: a `lax.ScatterDimensionNumbers` object that describes
      how dimensions of `operand`, `start_indices`, `updates` and the output
      relate.
    indices_are_sorted: whether `scatter_indices` is known to be sorted. If
      true, may improve performance on some backends.
    unique_indices: whether the elements to be updated in ``operand`` are
      guaranteed to not overlap with each other. If true, may improve performance on
      some backends. JAX does not check this promise: if the updated elements
      overlap when ``unique_indices`` is ``True`` the behavior is undefined.
    mode: how to handle indices that are out of bounds: when set to 'clip',
      indices are clamped so that the slice is within bounds, and when
      set to 'fill' or 'drop' out-of-bounds updates are dropped. The behavior
      for out-of-bounds indices when set to 'promise_in_bounds' is
      implementation-defined.

  Returns:
    An array containing the product of `operand` and the scattered updates.
  """
  jaxpr, consts = lax._reduction_jaxpr(lax.mul, typeof(lax._const(operand, 1)))
  operand, scatter_indices, updates = core.auto_insert_reshard(
      operand, scatter_indices, updates)
  return scatter_mul_p.bind(
      operand, scatter_indices, updates, update_jaxpr=jaxpr,
      update_consts=consts, dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=GatherScatterMode.from_any(mode))

