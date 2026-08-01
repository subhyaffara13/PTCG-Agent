
def _check_mesh_unreduced(mesh, pspec):
  for u in pspec.unreduced:
    if u not in mesh.axis_names:
      raise ValueError(
          f'Unreduced axes {u} is not found in {mesh.axis_names=}. '
          f'Got {pspec=}')
    if mesh._name_to_type[u] in (AxisType.Auto, AxisType.Manual):
      raise ValueError(
          'Unreduced axes can only refer to mesh axes that is of type'
          f' `Explicit`. Got unreduced axes: {pspec.unreduced} and'
          f' mesh: {mesh}')

  for u in pspec.reduced:
    if u not in mesh.axis_names:
      raise ValueError(
          f'Reduced axes {u} is not found in {mesh.axis_names=}. '
          f'Got {pspec=}')
    if mesh._name_to_type[u] in (AxisType.Auto, AxisType.Manual):
      raise ValueError(
          'Reduced axes can only refer to mesh axes that is of type'
          f' `Explicit`. Got reduced axes: {pspec.reduced} and'
          f' mesh: {mesh}')

