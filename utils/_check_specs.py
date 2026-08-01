
def _check_specs(error_type: SpecErrorType, specs: Any, manual_axes) -> None:
  from jax._src.hijax import HiPspec
  if error_type == SpecErrorType.input and specs is None:
    raise TypeError(
        "shard_map in_specs argument must be a pytree of "
        "`jax.sharding.PartitionSpec` instances, but it was None.\n"
        "Instead of `in_specs=None`, did you mean `in_specs=P()`, "
        "where `P = jax.sharding.PartitionSpec`?")

  def check_spec(p):
    if isinstance(p, HiPspec):
      return True  # TODO(mattjj,yashkatariya): add user validation method
    if not isinstance(p, PartitionSpec):
      return False
    for names in p.partitions:
      names = (names,) if not isinstance(names, tuple) else names
      for name in names:
        if name is not None and name not in manual_axes:
          return False
    return True

  if all(check_spec(p) for p in tree_leaves(specs)):
    return
  prefix = 'in' if error_type == SpecErrorType.input else 'out'
  msgs = [f"  {prefix}_specs{keystr(key)} is {x} of type {type(x).__name__}, "
          for key, x in generate_key_paths(specs) if not isinstance(x, P)]
  if not msgs:
    for key, p in generate_key_paths(specs):
      for names in p:
        names = (names,) if not isinstance(names, tuple) else names
        for name in names:
          if name is not None and name not in manual_axes:
            msgs.append(f"  {prefix}_specs{keystr(key)} refers to {repr(name)}")
    raise ValueError(
        f"shard_map {prefix}_specs argument must refer to an axis "
        f"marked as manual ({manual_axes}), but:\n\n"
        + '\n\n'.join(msgs) + '\n\n'
        f"Check the {prefix}_specs values passed to shard_map.")
  raise TypeError(
      f"shard_map {prefix}_specs argument must be a pytree of "
      f"`jax.sharding.PartitionSpec` instances, but:\n\n"
      + '\n\n'.join(msgs) + '\n\n'
      f"Check the {prefix}_specs values passed to shard_map.")

