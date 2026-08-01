
def _get_sdy_array_list_for_callbacks(avals: Sequence[core.ShapedArray]) -> SdyArrayList:
  """Returns an SdyArrayList with `max(1, len(avals))` replicated shardings."""
  ndims = [0]
  if avals:
    ndims = [x.ndim for x in avals if isinstance(x, core.ShapedArray)]
  return SdyArrayList(tuple(
      SdyArray(
          mesh_shape=(),
          dim_shardings=(SdyDim(axes=(), is_open=False),) * ndim,
          logical_device_ids=())
      for ndim in ndims))

