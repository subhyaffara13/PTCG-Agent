
def _scatter_addsub_jvp(
    prim, primals, tangents, *, update_jaxpr, update_consts, dimension_numbers,
    indices_are_sorted, unique_indices, mode):
  operand, indices, updates = primals
  g_operand, g_indices, g_updates = tangents
  del g_indices  # ignored
  val_out = prim.bind(
      operand, indices, updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode)
  if type(g_operand) is ad_util.Zero and type(g_updates) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    g_operand = ad.instantiate_zeros(g_operand)
    g_updates = ad.instantiate_zeros(g_updates)
    tangent_out = prim.bind(
        g_operand, indices, g_updates, update_jaxpr=update_jaxpr,
        update_consts=update_consts, dimension_numbers=dimension_numbers,
        indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
        mode=mode)
  return val_out, tangent_out

