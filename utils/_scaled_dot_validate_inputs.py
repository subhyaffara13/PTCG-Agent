
def _scaled_dot_validate_inputs(
    lhs: Array,
    rhs: Array,
    lhs_scale: Array | None,
    rhs_scale: Array | None,
    *,
    dimension_numbers: lax.DotDimensionNumbers,
    preferred_element_type: DTypeLike | None,
):
  """Validates the inputs to scaled_dot."""
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers

  ndims = [lhs.ndim, rhs.ndim]
  if lhs_scale is not None:
    ndims.append(lhs_scale.ndim)
  if rhs_scale is not None:
    ndims.append(rhs_scale.ndim)

  if max(ndims) != min(ndims):
    raise TypeError(
        "All input tensors must have the same rank. Got lhs rank:"
        f" {lhs.ndim} rhs rank: {rhs.ndim} lhs_scale rank:"
        f" {lhs_scale.ndim if lhs_scale is not None else 'N/A'} rhs_scale"
        f" rank: {rhs_scale.ndim if rhs_scale is not None else 'N/A'}."
    )

  if len(lhs_batch) != len(rhs_batch):
    raise TypeError(
        "LHS and RHS must have the same number of batch dimensions, got"
        f" {len(lhs_batch)} and {len(rhs_batch)}."
    )
  if len(lhs_contracting) != len(rhs_contracting):
    raise TypeError(
        "LHS and RHS must have the same number of contracting dimensions, got"
        f" {len(lhs_contracting)} and {len(rhs_contracting)}."
    )

  for i_lhs, i_rhs in zip(lhs_batch, rhs_batch):
    batch_dims_sizes = [
        lhs.shape[i_lhs],
        rhs.shape[i_rhs],
    ]
    if lhs_scale is not None:
      batch_dims_sizes.append(lhs_scale.shape[i_lhs])
    if rhs_scale is not None:
      batch_dims_sizes.append(rhs_scale.shape[i_rhs])
    if max(batch_dims_sizes) != min(batch_dims_sizes):
      raise TypeError(
          "All input tensors must have the same batch dimension size for"
          f" batch dims ({i_lhs}, {i_rhs})."
      )

  # Check contracting dimensions are the same.
  for i, j in zip(lhs_contracting, rhs_contracting):
    if lhs.shape[i] != rhs.shape[j]:
      raise TypeError(
          f"LHS contracting dim {i} of size"
          f" {lhs.shape[i]} does not match RHS"
          f" contracting dim {j} of size"
          f" {rhs.shape[j]}."
      )

  if lhs_scale is not None:
    _validate_operand_scale("LHS", lhs, lhs_scale, lhs_contracting)

  if rhs_scale is not None:
    _validate_operand_scale("RHS", rhs, rhs_scale, rhs_contracting)

