
def _scatter_extremal_jvp(scatter_op, primals, tangents, update_jaxpr,
                          update_consts, dimension_numbers,
                          indices_are_sorted, unique_indices, mode):
  operand, indices, updates = primals
  g_operand, g_indices, g_updates = tangents

  scatter_dnums = dimension_numbers
  updates_shape = updates.shape

  val_out = scatter_op.bind(
      operand, indices, updates, update_jaxpr=update_jaxpr,
      update_consts=update_consts, dimension_numbers=scatter_dnums,
      indices_are_sorted=indices_are_sorted,
      unique_indices=unique_indices, mode=mode)

  if type(g_operand) is ad_util.Zero and type(g_updates) is ad_util.Zero:
    tangent_out = ad_util.p2tz(val_out)
  else:
    g_operand = ad.instantiate_zeros(g_operand)
    g_updates = ad.instantiate_zeros(g_updates)

    # gather_dnums and slice_sizes define the gather op that is the inverse of
    # the scatter op specified by scatter_dnums
    gather_dnums = GatherDimensionNumbers(
        offset_dims=scatter_dnums.update_window_dims,
        collapsed_slice_dims=scatter_dnums.inserted_window_dims,
        start_index_map=scatter_dnums.scatter_dims_to_operand_dims,
        operand_batching_dims=scatter_dnums.operand_batching_dims,
        start_indices_batching_dims=scatter_dnums.scatter_indices_batching_dims,
    )

    slice_sizes = []
    pos = 0
    for i in range(len(operand.shape)):
      if (
          i in scatter_dnums.inserted_window_dims
          or i in scatter_dnums.operand_batching_dims
      ):
        slice_sizes.append(1)
      else:
        slice_sizes.append(updates_shape[scatter_dnums.update_window_dims[pos]])
        pos += 1

    # For consistency with other max operations, if there are two or more values
    # in updates that are contending to replace the same index location, the
    # resulting tangent at that location will be the average of the associated
    # tangents for the values in updates.

    initial_vals = gather(
        operand, indices, gather_dnums, slice_sizes)

    target_vals = gather(
        val_out, indices, gather_dnums, slice_sizes)

    successful_updates = (updates == target_vals)
    retained_values = (initial_vals == target_vals)

    num_updates = gather(
        scatter_add(
            lax._zeros(operand), indices,
            lax.select(successful_updates, lax._ones(updates),
                       lax._zeros(updates)),
            scatter_dnums),
        indices,
        gather_dnums,
        slice_sizes)

    num_refs = gather(
        scatter_add(lax._zeros(operand),
                    indices,
                    lax._ones(updates),
                    scatter_dnums),
        indices,
        gather_dnums,
        slice_sizes)

    updates_normalizer = lax.select(retained_values,
                                    1.0 / (num_updates + 1),
                                    1.0 / num_updates)

    updates_coef = lax.select(successful_updates,
                              updates_normalizer,
                              lax._zeros(updates))

    operand_normalizer = lax.select(retained_values,
                                    1.0 / (num_updates + 1),
                                    lax._zeros(num_updates))

    operand_coef = (-1.0 + operand_normalizer) / num_refs

    # This can be simplified once scatter has transpose implemented
    target_tangents = gather(
        g_operand, indices, gather_dnums, slice_sizes)

    tangent_updates = (target_tangents * operand_coef +
                       g_updates * updates_coef)

    tangent_out = scatter_add(g_operand,
                              indices,
                              tangent_updates,
                              scatter_dnums,
                              indices_are_sorted=indices_are_sorted,
                              unique_indices=unique_indices,
                              mode=mode)

  return val_out, tangent_out

