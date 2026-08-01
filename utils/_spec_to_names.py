
def _spec_to_names(spec: PartitionSpec):
  return {i: names if isinstance(names, tuple) else (names,)
          for i, names in enumerate(spec.partitions) if names is not None}

