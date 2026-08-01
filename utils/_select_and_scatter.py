
def _select_and_scatter(operand: Array, select: Callable,
                        window_dimensions: core.Shape,
                        window_strides: Sequence[int],
                        padding: Sequence[tuple[int, int]], source: Array,
                        init_value: Array, scatter: Callable) -> Array:
  select_jaxpr, select_consts = lax._reduction_jaxpr(
    select, core.typeof(init_value))
  scatter_jaxpr, scatter_consts = lax._reduction_jaxpr(
    scatter, core.typeof(init_value))
  operand, source, init_value = core.auto_insert_reshard(
      operand, source, init_value)
  return select_and_scatter_p.bind(
      operand, source, init_value, select_jaxpr=select_jaxpr,
      select_consts=select_consts, scatter_jaxpr=scatter_jaxpr,
      scatter_consts=scatter_consts, window_dimensions=tuple(window_dimensions),
      window_strides=tuple(window_strides), padding=tuple(padding))

