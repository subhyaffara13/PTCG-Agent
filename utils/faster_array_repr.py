
def faster_array_repr(array: jax.Array) -> str:
  """Computes ``repr(array)``, only copying the rendered array elements.

  ``repr(array)`` on a very large jax Array can be slow, because it copies the
  entire array to host memory even when only a few elements are actually needed.
  We can avoid this by truncating the array on device before fetching it.

  Args:
    array: The array to summarize.

  Returns:
    A string representation of the array. May differ slightly from the ordinary
    ``repr``, but should contain the same elements.
  """
  assert jax is not None, "JAX is not available."
  jnp = jax.numpy
  if array.size < np.get_printoptions()["threshold"]:
    return repr(array)

  if array.aval is not None and array.aval.weak_type:
    dtype_str = f"dtype={array.dtype.name}, weak_type=True)"
  else:
    dtype_str = f"dtype={array.dtype.name})"

  edgeitems = np.get_printoptions()["edgeitems"]
  edge_items_per_axis = []
  for size in array.shape:
    if size > 2 * edgeitems + 1:
      edge_items_per_axis.append(edgeitems)
    else:
      edge_items_per_axis.append(None)
  array_edges, _ = truncate_array_and_mask(
      array,
      np.ones((1,) * array.ndim, dtype=jnp.bool_),
      edge_items_per_axis=tuple(edge_items_per_axis),
  )
  prefix = "Array("
  datastring = np.array2string(
      np.array(array_edges),
      prefix=prefix,
      suffix=",",
      separator=", ",
      threshold=0,
      edgeitems=edgeitems,
  )
  return f"{prefix}{datastring}, {dtype_str}"

