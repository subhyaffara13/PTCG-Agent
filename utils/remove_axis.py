
def remove_axis(tree: Any, index: int, params: dict[Any, Any]) -> Any:
  """Remove an axis from each AxisMetadata node in a PyTree."""
  return map_axis_meta(lambda x: x.remove_axis(index, params), tree)


def remove_axis(
  tree: A, index: int, transform_metadata: tp.Mapping[tp.Any, tp.Any]
) -> A:
  axis_name, other_meta = _get_partition_name_and_metadata(transform_metadata)

  def remove_field(fields, index, value):
    iterable = list(fields)
    removed = iterable.pop(index)
    if removed != value:
      raise ValueError(
        f'Expected to remove {value!r} at index {index} from '
        f'{fields!r}, but found {removed!r}.'
      )
    return tuple(iterable)

  def _remove_axis(x: tp.Any):
    if isinstance(x, variablelib.Variable):
      if hasattr(x, 'out_sharding') and x.out_sharding is not None:
        x.set_metadata(
          out_sharding=remove_field(x.out_sharding, index, axis_name)
        )

      for k, v in other_meta.items():
        if hasattr(x, k) and (t := getattr(x, k)) and isinstance(t, tuple):
          x.set_metadata(k, remove_field(t, index, v))

      x.remove_axis(index, axis_name)
    return x

  return jax.tree.map(
    _remove_axis,
    tree,
    is_leaf=lambda x: isinstance(x, variablelib.Variable),
  )

