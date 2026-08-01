
def _stack_sparse(spenv, *spvalues, axis, broadcast_in_dim, concatenate):
  arrays = spvalues_to_arrays(spenv, spvalues)
  base_shape = arrays[0].shape
  new_shape = base_shape[:axis] + (1,) + base_shape[axis:]
  bdims = [d if d < axis else d + 1 for d in range(arrays[0].ndim)]
  expanded = [
    broadcast_in_dim(x, shape=new_shape, broadcast_dimensions=bdims)
    for x in arrays
  ]
  return arrays_to_spvalues(spenv, [concatenate(expanded, dimension=axis)])

