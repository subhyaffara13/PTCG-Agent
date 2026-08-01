
def prepare_axis_resources(axis_resources, arg_name,
                           allow_unconstrained_dims=False):
  entries, treedef = tree_util.tree_flatten(
      axis_resources, is_leaf=lambda x: x is None)
  what = f"{arg_name} leaf specifications"

  new_entries: list[Any] = []
  for entry in entries:
    if isinstance(entry, UnspecifiedValue) or entry is None:
      new_entries.append(entry)
    elif isinstance(entry, jsharding.Sharding):
      if isinstance(entry, NamedSharding) and entry.mesh.empty:
        raise ValueError(f'One of {what} got an empty NamedSharding: {entry} '
                         'which is not allowed.')
      if (not allow_unconstrained_dims and isinstance(entry, NamedSharding) and
          PartitionSpec.UNCONSTRAINED in entry.spec.partitions):
        raise ValueError(
            f'Unconstrained dims are not allowed when passed to {arg_name}:'
            f' {entry}')
      new_entries.append(entry)
    else:
      if not isinstance(entry, PartitionSpec):
        raise TypeError(f"{what} are expected to be "
                        f"PartitionSpec instances or None, but got {entry}")
      if (not allow_unconstrained_dims and
          PartitionSpec.UNCONSTRAINED in entry.partitions):
        raise ValueError(
            f'Unconstrained dims are not allowed when passed to {arg_name}:'
            f' {entry}')
      _check_unique_resources(entry, arg_name)
      new_entries.append(entry)
  return tree_util.tree_unflatten(treedef, new_entries)

