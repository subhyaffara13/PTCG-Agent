from typing import Any

def add_axis(tree: Any, index: int, params: dict[Any, Any]) -> Any:
  """Add an axis to each AxisMetadata node in a PyTree."""
  return map_axis_meta(lambda x: x.add_axis(index, params), tree)


def add_axis(tree: A, index: int, transform_metadata: tp.Mapping) -> A:
  axis_name, other_meta = _get_partition_name_and_metadata(transform_metadata)

  def insert_field(fields, index, value):
    iterable = list(fields)
    while len(iterable) < index:
      iterable.append(None)
    iterable.insert(index, value)
    return tuple(iterable)

  def _add_axis(x: tp.Any):
    if isinstance(x, variablelib.Variable):
      metadata = x.get_metadata()
      if 'out_sharding' in metadata and metadata['out_sharding']:
        sharding = metadata['out_sharding']
        x.set_metadata(out_sharding=insert_field(sharding, index, axis_name))

      for k, v in other_meta.items():
        if hasattr(x, k) and (t := getattr(x, k)) and isinstance(t, tuple):
          x.set_metadata(k, insert_field(t, index, v))

      assert isinstance(x, variablelib.Variable)
      x.add_axis(index, axis_name)
    return x

  return jax.tree.map(
    _add_axis, tree, is_leaf=lambda x: isinstance(x, variablelib.Variable)
  )

