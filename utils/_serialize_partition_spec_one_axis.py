
def _serialize_partition_spec_one_axis(builder: flatbuffers.Builder,
                                       spec: str | tuple[str, ...] | None) -> int:
  if spec is None:
    axes = ()
  else:
    axes = (spec,) if isinstance(spec, str) else spec

  axes_offset = _serialize_array(builder,
                                 lambda builder, ps: builder.CreateString(ps),
                                 axes)
  ser_flatbuf.PartitionSpecOneAxisStart(builder)
  ser_flatbuf.PartitionSpecOneAxisAddAxes(builder, axes_offset)
  return ser_flatbuf.PartitionSpecOneAxisEnd(builder)

