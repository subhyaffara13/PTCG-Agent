
def vmap_with_axes(
    target: 'flax.linen.transforms.Target',
    variable_axes: Mapping[
        CollectionFilter, InOutAxis
    ],
    split_rngs: Mapping[PRNGSequenceFilter, bool] = {},
    in_axes=0,
    out_axes=0,
    axis_size: int | None = None,
    axis_name: str | None = None,
    partitioning_axis_names: Mapping[Any, str] = {},
    spmd_axis_name: str | None = None,
    methods=None,
) -> 'flax.linen.transforms.Target':
  """Wrapped version of nn.vmap that handles logical axis metadata."""

  # tell normal vmap to broadcast axis metadata.
  variable_axes = dict(variable_axes)  # shallow copy
  for name in partitioning_axis_names:
    variable_axes[f'{name}_axes'] = None

  # perform usual lifted vmap
  vmapped = flax.linen.transforms.lift_transform(
      flax.core.lift.vmap,
      target,
      variable_axes=variable_axes,
      split_rngs=split_rngs,
      in_axes=in_axes,
      out_axes=out_axes,
      axis_size=axis_size,
      axis_name=axis_name,
      spmd_axis_name=spmd_axis_name,
      methods=methods,
  )

  for collection_name, axis in variable_axes.items():
    if collection_name in partitioning_axis_names:
      vmapped = _add_axis_to_metadata(  # pylint: disable=protected-access
          vmapped,
          axis_pos=axis,
          axis_name=partitioning_axis_names[collection_name],
          axis_col=f'{collection_name}_axes',
      )

  return vmapped

