
def logical_to_mesh_axes(
  array_dim_names: Sequence[str | None] | None,
  rules: LogicalRules | None = None,
) -> jax.sharding.PartitionSpec | None:
  """Compute layout for an array.

  The rules are in order of precedence, and consist of pairs:
  ``(ArrayDimensionName, MeshDimensionName)``, meaning that the given array
  dimension (if present and unused) should be sharded across the given
  mesh dimension (if present and unused).

  A Layout of an Array is expressed as a tuple with one element for each
  dimension in the Array. The element is either None, or is the name of a
  mesh-dimension, meaning that this dimension of the array is sharded across
  this dimension of the mesh.

  For example, given an array with::

    array_dim_names = ('batch', 'length', 'heads', 'features')

  and the layout rules are::

    rules = (('batch', 'X'),
             ('features', 'X'),
             ('heads', 'Y'),
             ('batch', 'Z'))

  then this function will return::

    PartitionSpec('X', None, 'Y', None)

  Args:
    array_dim_names: Tuple of array dimension names or None.
    rules: Optional logical to mesh rules override.  Defaults to using the
      rules defined in the dynamic context set from the ``axis_rules`` function.

  Returns:
    PartitionSpec for the parameter.
  """
  result = _logical_to_mesh_axes(array_dim_names, rules)
  if result is None:
    return None
  # We default to None - ie unsharded along the dimension.
  result = [None if x is _unassigned_axis else x for x in result]
  return jax.sharding.PartitionSpec(*result)

