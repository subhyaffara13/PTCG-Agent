
def _get_partition_name_and_metadata(
  transform_metadata: tp.Mapping[tp.Any, tp.Any],
) -> tuple[str, tp.Mapping[tp.Any, tp.Any]]:
  if PARTITION_NAME not in transform_metadata:
    raise ValueError(
      'Trying to transform a Partitioned variable but "partition_name" '
      f'is not specified in transform_metadata: {transform_metadata}'
    )
  other_meta = dict(transform_metadata)  # shallow copy
  other_meta.pop(PARTITION_NAME)
  return transform_metadata[PARTITION_NAME], other_meta

