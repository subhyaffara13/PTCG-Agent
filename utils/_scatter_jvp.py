
def _scatter_jvp(primals, tangents, *, update_jaxpr, update_consts,
                 dimension_numbers, indices_are_sorted, unique_indices,
                 mode):
  if update_jaxpr is not None:
    raise NotImplementedError("scatter_apply JVP not implemented")
  operand, indices, updates = primals
  g_operand, g_indices, g_updates = tangents
  dnums = dimension_numbers

  if type(g_operand) is ad_util.Zero and type(g_updates) is ad_util.Zero:
    val_out = scatter_p.bind(
      operand, indices, updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode)
    return val_out, ad_util.p2tz(val_out)

  g_operand = ad.instantiate_zeros(g_operand)
  g_updates = ad.instantiate_zeros(g_updates)

  if unique_indices:
    # If the user has promised that the updates don't overlap, we can use a much
    # simpler JVP.
    val_out = scatter_p.bind(
      operand, indices, updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=True, mode=mode)
    tangent_out = scatter_p.bind(
      g_operand, indices, g_updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=dnums,
      indices_are_sorted=indices_are_sorted, unique_indices=True, mode=mode)
    return val_out, tangent_out

  # If there are overlapping indices in the scatter, it is unspecified which
  # update "wins". So we use the following perhaps surprising scheme:
  # a) attach a positive ID to each update in updates, and perform the scatter
  #    on the IDs
  # b) perform the inverse gather on the scattered IDs (similar to
  #    _scatter_add_transpose).
  # c) use the gathered IDs to mask the primal and tangent values.
  # d) perform a scatter-add on the masked primal and tangent values. A benefit
  #    of using scatter-add here is that we don't need a `scatter` transpose
  #    rule.

  # a) attach a positive ID to each update in `updates`, and perform a scatter
  #    on the IDs.
  ids_shape = list(updates.shape)
  for update_dim in dnums.update_window_dims:
    ids_shape[update_dim] = 1
  num_ids = math.prod(ids_shape)
  id_dtype = lax_utils.int_dtype_for_dim(num_ids, signed=False)
  update_ids = lax.add(lax.reshape(lax.iota(id_dtype, num_ids), ids_shape),
                       lax._ones(updates, dtype=id_dtype))

  scattered_ids = scatter(lax.full(operand.shape, 0, id_dtype),
                          indices, update_ids, dnums,
                          indices_are_sorted=indices_are_sorted,
                          unique_indices=unique_indices, mode=mode)

  # b) compute the inverse gather that "undoes" the scatter on the id values.
  gather_dnums = GatherDimensionNumbers(
      offset_dims=dnums.update_window_dims,
      collapsed_slice_dims=dnums.inserted_window_dims,
      start_index_map=dnums.scatter_dims_to_operand_dims,
      operand_batching_dims=dnums.operand_batching_dims,
      start_indices_batching_dims=dnums.scatter_indices_batching_dims,
  )
  slice_sizes = []
  pos = 0
  for i in range(len(scattered_ids.shape)):
    if i in dnums.inserted_window_dims or i in dnums.operand_batching_dims:
      slice_sizes.append(1)
    else:
      slice_sizes.append(updates.shape[dnums.update_window_dims[pos]])
      pos += 1
  gathered_update_ids = gather(scattered_ids, indices,
                               dimension_numbers=gather_dnums,
                               slice_sizes=slice_sizes)

  # c) mask off input elements that do not correspond to a primal output.
  masked_operand = lax.select(lax.eq(scattered_ids, lax._zeros(scattered_ids)),
                              operand, lax._zeros(operand))
  masked_updates = lax.select(lax.eq(update_ids,  gathered_update_ids),
                              updates, lax._zeros(updates))
  masked_g_operand = lax.select(lax.eq(scattered_ids, lax._zeros(scattered_ids)),
                                g_operand, lax._zeros(g_operand))
  masked_g_updates = lax.select(lax.eq(update_ids, gathered_update_ids),
                                g_updates, lax._zeros(g_updates))

  # d) perform scatter-adds to compute the primal and tangent outputs.
  val_out = scatter_add(masked_operand, indices, masked_updates,
                        dimension_numbers=dnums,
                        indices_are_sorted=indices_are_sorted,
                        unique_indices=unique_indices, mode=mode)
  tangent_out = scatter_add(masked_g_operand, indices, masked_g_updates,
                            dimension_numbers=dnums,
                            indices_are_sorted=indices_are_sorted,
                            unique_indices=unique_indices, mode=mode)
  return val_out, tangent_out

