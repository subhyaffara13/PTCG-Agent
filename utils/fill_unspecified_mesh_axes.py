
def fill_unspecified_mesh_axes(
    parallelism_vals, target_product, parallelism_type='ICI'
):
  """Evaluates unspecified DCN/ICI parallelism values."""
  if -1 in parallelism_vals:
    assert parallelism_vals.count(-1) == 1, (
        f'Found unspecified values (-1) for more than one {parallelism_type}   '
        '   parallelism axis. At most one axis can be unspecified.'
    )

    determined_val = target_product / np.prod(parallelism_vals) * -1

    assert determined_val >= 1 and determined_val.is_integer, (
        'Unspecified value unable to be determined with the given     '
        f' {parallelism_type} parallelism values'
    )

    parallelism_vals[parallelism_vals.index(-1)] = int(determined_val)

  assert np.prod(parallelism_vals) == target_product, (
      f'Number of devices per slice {target_product} does not match the product'
      f' of the {parallelism_type} parallelism {np.prod(parallelism_vals)}'
  )

  return parallelism_vals

