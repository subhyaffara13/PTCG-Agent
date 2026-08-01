
def _ragged_dot_general_jvp_rule(
    primals, tangents, ragged_dot_dimension_numbers,
    precision, preferred_element_type, group_offset, out_sharding
):
  # note - we could ostensibly just get this by passing on the
  # value to ragged_dot below, but, this feels cleaner.
  if group_offset is not None:
    raise NotImplementedError('Unimplemented group_offset support.')
  x, y, gs = primals
  dx, dy, _ = tangents  # no tan on the gs

  # primal
  primal_out = ragged_dot_general(
      x,
      y,
      gs,
      ragged_dot_dimension_numbers=ragged_dot_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
  )

  # tangent
  dx_out = (
      ragged_dot_general(
          dx,
          y,
          gs,
          ragged_dot_dimension_numbers=ragged_dot_dimension_numbers,
          precision=precision,
          preferred_element_type=preferred_element_type,
      )
      if type(dx) is not ad_util.Zero
      else _zeros(primal_out)
  )
  dy_out = (
      ragged_dot_general(
          x,
          dy,
          gs,
          ragged_dot_dimension_numbers=ragged_dot_dimension_numbers,
          precision=precision,
          preferred_element_type=preferred_element_type,
      )
      if type(dy) is not ad_util.Zero
      else _zeros(primal_out)
  )
  tangent_out = add(dx_out, dy_out)

  return primal_out, tangent_out

