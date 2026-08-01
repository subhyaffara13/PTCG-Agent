
def _select_and_scatter_add(source: Array, operand: Array,
                            select_prim: core.Primitive,
                            window_dimensions: core.Shape,
                            window_strides: Sequence[int],
                            padding: Sequence[tuple[int, int]]) -> Array:
  source, operand = core.auto_insert_reshard(source, operand)
  return select_and_scatter_add_p.bind(
      source, operand, select_prim=select_prim,
      window_dimensions=tuple(window_dimensions),
      window_strides=tuple(window_strides), padding=tuple(padding))

