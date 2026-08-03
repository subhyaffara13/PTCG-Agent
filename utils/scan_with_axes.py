from typing import Any, Callable

def scan_with_axes(
    target: 'flax.linen.transforms.Target',
    variable_axes: Mapping[
        CollectionFilter, InOutScanAxis
    ] = {},
    variable_broadcast: CollectionFilter = False,
    variable_carry: CollectionFilter = False,
    split_rngs: Mapping[PRNGSequenceFilter, bool] = {},
    in_axes=0,
    out_axes=0,
    length: int | None = None,
    reverse: bool = False,
    unroll: int = 1,
    axis_name: str = 'layers',
    axes_collections: tuple[str, ...] = ('params',),
    data_transform: Callable[..., Any] | None = None,
    methods=None,
) -> 'flax.linen.transforms.Target':
  """Wrapped version of nn.scan that handles logical axis metadata."""

  # we broadcast the static metadata collections.
  axes_filters = tuple(f'{col}_axes' for col in axes_collections)
  variable_broadcast = flax.core.scope.union_filters(
      variable_broadcast, axes_filters
  )

  # perform usual lifted scan
  scanned = flax.linen.transforms.lift_transform(
      flax.core.lift.scan,
      target,
      variable_axes=variable_axes,
      variable_broadcast=variable_broadcast,
      variable_carry=variable_carry,
      split_rngs=split_rngs,
      in_axes=in_axes,
      out_axes=out_axes,
      length=length,
      reverse=reverse,
      unroll=unroll,
      data_transform=data_transform,
      methods=methods,
  )

  # add scan axis to logical axes metadata
  for col in axes_collections:
    if col in variable_axes:
      scanned = _add_axis_to_metadata(
          scanned,
          axis_pos=variable_axes[col],
          axis_name=axis_name,
          axis_col=f'{col}_axes',
      )
  return scanned

