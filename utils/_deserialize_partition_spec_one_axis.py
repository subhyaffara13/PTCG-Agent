
def _deserialize_partition_spec_one_axis(
    spec: ser_flatbuf.PartitionSpecOneAxis) -> str | tuple[str, ...] | None:
  axes = tuple(spec.Axes(i).decode("utf-8") for i in range(spec.AxesLength()))
  if not axes:
    return None
  else:
    return axes[0] if len(axes) == 1 else axes

