
def _select_and_gather_add(tangents: Array, operand: Array,
                           select_prim: core.Primitive,
                           window_dimensions: core.Shape,
                           window_strides: Sequence[int],
                           padding: Sequence[tuple[int, int]],
                           base_dilation: Sequence[int],
                           window_dilation: Sequence[int]) -> Array:
  """Extracts the tangent corresponding to the minimum or maximum element in
  each window of the `operand` array.

  Wraps XLA's `ReduceWindow
  <https://www.openxla.org/xla/operation_semantics#reducewindow>`_
  operator, which applies a reduction function to all elements in each window of
  the input multi-dimensional array. In this case, the input multi-dimensional
  array is built by packing each element in the `operand` array with its
  corresponding element in the `tangents` array.

  Args:
    tangents: an array
    operand: an array with the same shape as `tangents`
    select_prim: a reduction function (restricted to `ge_p` and `le_p`)
    window_dimensions: an array of integers for window dimension values
    window_strides: an array of integers for window stride values
    base_dilation: an array of integers for base dilation values
    window_dilation: an array of integers for window dilation values

  Returns:
    An array containing the elements in `tangents` corresponding to the output
    of the reduction of `operand` fin each window.
  """
  tangents, operand = core.auto_insert_reshard(tangents, operand)
  return select_and_gather_add_p.bind(
      tangents, operand, select_prim=select_prim,
      window_dimensions=tuple(window_dimensions),
      window_strides=tuple(window_strides), padding=tuple(padding),
      base_dilation=tuple(base_dilation),
      window_dilation=tuple(window_dilation))

