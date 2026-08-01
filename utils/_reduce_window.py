
def _reduce_window(
    operand,
    init_value,
    computation,
    window_dimensions: core.Shape,
    window_strides: Sequence[int] | None,
    padding: str | Sequence[tuple[int, int]],
    base_dilation: Sequence[int] | None = None,
    window_dilation: Sequence[int] | None = None,
):
  flat_operands, operand_tree = tree_util.tree_flatten(operand)
  comp_debug = api_util.debug_info("reduce_window comp", computation,
                                   (init_value, init_value), {})
  flat_init_values, init_value_tree = tree_util.tree_flatten(init_value)
  if operand_tree != init_value_tree:
    raise ValueError(
        "Operands must have the same tree structure as "
        f"init_values: {operand_tree} vs. {init_value_tree}"
    )
  if len(flat_operands) != len(flat_init_values):
    raise ValueError(
        "Must have same total number of operands as init_values: "
        f" {len(flat_operands)} vs. {len(flat_init_values)}"
    )

  if len(flat_operands) == 0:
    raise ValueError("reduce_window must have at least one operand.")
  if isinstance(padding, str):
    dilated_window_dims = (
        window_dimensions if window_dilation is None else
        lax._dilate_shape(window_dimensions, window_dilation))
    padding = tuple(lax.padtype_to_pads(
        flat_operands[0].shape, dilated_window_dims, window_strides or [], padding))
  else:
    padding = tuple((x, y) for x, y in padding)
  if window_strides is None:
    window_strides = (1,) * len(window_dimensions)
  if base_dilation is None:
    base_dilation = (1,) * len(window_dimensions)
  if window_dilation is None:
    window_dilation = (1,) * len(window_dimensions)
  monoid_reducer = _get_monoid_window_reducer(computation, flat_init_values)
  if monoid_reducer:
    return monoid_reducer(operand, window_dimensions, window_strides, padding,
                          base_dilation, window_dilation)
  else:
    flat_init_avals = map(core.typeof, flat_init_values)
    jaxpr, out_tree = lax._variadic_reduction_jaxpr(
        computation, comp_debug, tuple(flat_init_avals), init_value_tree
    )
    if operand_tree != out_tree:
      raise ValueError(
        'reduce_window output must have the same tree structure as the operands'
        f' {operand_tree} vs. {out_tree}')
    flat_operands = core.auto_insert_reshard(*flat_operands)
    out_flat = reduce_window_p.bind(
        *flat_operands,
        *flat_init_values,
        jaxpr=jaxpr.jaxpr,
        consts=tuple(jaxpr.consts),
        window_dimensions=tuple(window_dimensions),
        window_strides=tuple(window_strides),
        padding=padding,
        base_dilation=tuple(base_dilation),
        window_dilation=tuple(window_dilation),
    )
    return tree_util.tree_unflatten(out_tree, out_flat)

