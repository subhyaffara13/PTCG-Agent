
def _deserialize_partition_spec(spec: ser_flatbuf.PartitionSpec
                                ) -> partition_spec.PartitionSpec:
  partitions = tuple(_deserialize_partition_spec_one_axis(spec.Partitions(i))
                     for i in range(spec.PartitionsLength()))
  reduced = frozenset(spec.Reduced(i).decode("utf-8")
                      for i in range(spec.ReducedLength()))
  unreduced = frozenset(spec.Unreduced(i).decode("utf-8")
                        for i in range(spec.UnreducedLength()))
  return partition_spec.PartitionSpec(*partitions,
                                      reduced=reduced,
                                      unreduced=unreduced)

