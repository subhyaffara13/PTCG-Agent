
def render_array_sharding(
    array: ArrayInRegistry,
    rows: Sequence[int | AxisName] = (),
    columns: Sequence[int | AxisName] = (),
) -> figures_impl.TreescopeFigure:
  """Renders the sharding of an array.

  Args:
    array: The array whose sharding we should render.
    rows: Optional explicit ordering of axes for the visualization rows.
    columns: Optional explicit ordering of axes for the visualization columns.

  Returns:
    A rendering of that array's sharding.
  """
  # Retrieve the adapter for this array, which we will use to construct
  # the rendering.
  type_registries.update_registries_for_imports()
  adapter = type_registries.lookup_ndarray_adapter(array)
  if adapter is None:
    raise TypeError(
        "Cannot render sharding for array with unrecognized type"
        f" {type(array)} (not found in array adapter registry)"
    )

  # Extract information about axis names, indices, and sizes, along with the
  # sharding info.
  array_axis_info = adapter.get_axis_info_for_array_data(array)
  sharding_info = adapter.get_sharding_info_for_array_data(array)
  if sharding_info is None:
    raise ValueError(
        "Cannot render sharding for array without sharding info (not provided"
        f" by array adapter for {type(array)})."
    )

  return render_sharding_info(
      array_axis_info=array_axis_info,
      sharding_info=sharding_info,
      rows=rows,
      columns=columns,
  )

