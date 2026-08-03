from typing import Any

def add_metadata_axis(
  target: Target,
  variable_axes: Mapping[CollectionFilter, InOutAxis] = FrozenDict(),
  metadata_params: dict[Any, Any] = {},
) -> Target:
  """A helper to manipulate boxed axis metadata.

  This is a helper to manipulate the *metadata* in boxed variables, similar
  to how lifted ``vmap`` and ``scan`` will handle the introduction and stripping
  of the new metadata axis across a transform boundary.

  Args:
    target: a ``Module`` or a function taking a ``Module``
      as its first argument.
    variable_axes: the variable collections whose axis metadata is being
      transformed. Use `None` to indicate a broadcasted collection or an integer
      to specify an axis index for an introduced axis.
    methods: If `target` is a `Module`, the methods of `Module` to vmap over.
    metadata_params: arguments dict passed to AxisMetadata instances in the
      variable tree.
  Returns:
    A transformed version of ``target`` that performs a transform of the
    axis metadata on its variables.
  """

  def add_fn(axis):
    return lambda x: meta.add_axis(x, axis, metadata_params)

  def remove_fn(axis):
    return lambda x: meta.remove_axis(x, axis, metadata_params)

  for col_name, axis in variable_axes.items():
    target = map_variables(
      target,
      col_name,
      trans_in_fn=remove_fn(axis),
      trans_out_fn=add_fn(axis),
      mutable=True,
    )
  return target

