
def _scatter_add_rule(primals_in, series_in, *, update_jaxpr, update_consts,
                      dimension_numbers, indices_are_sorted, unique_indices,
                      mode):
  bind = partial(lax.scatter_add_p.bind, update_jaxpr=update_jaxpr,
                 update_consts=update_consts, dimension_numbers=dimension_numbers,
                 indices_are_sorted=indices_are_sorted,
                 unique_indices=unique_indices, mode=mode)
  operand, scatter_indices, updates = primals_in
  primal_out = bind(operand, scatter_indices, updates)
  series_out = [bind(d1, scatter_indices, d2) for d1, _, d2 in zip(*series_in)]
  return primal_out, series_out

