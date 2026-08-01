
def _unravel_array_into_pytree(pytree, axis, example, arr, specs):
  """Unravel an array into a PyTree with a given structure.
  Args:
      pytree: The pytree that provides the structure.
      axis: The parameter axis is either -1, 0, or 1.  It controls the
        resulting shapes.
      example: If specified, cast the components to the matching dtype/weak_type,
        or else use the pytree leaf type if example is None.
      arr: The array to be unraveled.
  """
  leaves, treedef = tree_flatten(pytree)
  specs, _ = tree_flatten(specs)
  shapes = [arr.shape[:axis] + np.shape(l) + arr.shape[axis+1:] for l in leaves]
  parts = _split(arr, np.cumsum(map(np.size, leaves[:-1])), axis)
  reshaped_parts = [
      _possible_downcast(np.reshape(x, shape),
                         leaf if example is None else example,
                         spec=spec)
      for x, shape, leaf, spec in zip(parts, shapes, leaves, specs)]
  return tree_unflatten(treedef, reshaped_parts)

