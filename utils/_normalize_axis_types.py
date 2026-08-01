
def _normalize_axis_types(axis_names, axis_types, name):
  axis_types = ((AxisType.Auto,) * len(axis_names)
                if axis_types is None else axis_types)
  if not isinstance(axis_types, tuple):
    axis_types = (axis_types,)

  if not all(isinstance(a, AxisType) for a in axis_types):
    raise TypeError(
        f"axis_types passed to {name} must be of type `jax.sharding.AxisType`."
        f" Got {axis_types} of type {tuple(type(a) for a in axis_types)}")
  if len(axis_names) != len(axis_types):
    raise ValueError(
        "Number of axis names should match the number of axis_types. Got"
        f" axis_names={axis_names} and axis_types={axis_types}")
  return axis_types

