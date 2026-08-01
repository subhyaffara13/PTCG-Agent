
def _serialize_partition_spec(builder: flatbuffers.Builder,
                              spec: partition_spec.PartitionSpec) -> int:
  partitions = _serialize_array(builder, _serialize_partition_spec_one_axis,
                                spec._partitions)
  reduced = _serialize_array(builder,
                             lambda builder, ps: builder.CreateString(ps),
                             spec.reduced)
  unreduced = _serialize_array(builder,
                               lambda builder, ps: builder.CreateString(ps),
                               spec.unreduced)

  ser_flatbuf.PartitionSpecStart(builder)
  ser_flatbuf.PartitionSpecAddPartitions(builder, partitions)
  ser_flatbuf.PartitionSpecAddReduced(builder, reduced)
  ser_flatbuf.PartitionSpecAddUnreduced(builder, unreduced)
  return ser_flatbuf.PartitionSpecEnd(builder)

