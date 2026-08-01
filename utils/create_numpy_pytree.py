
def create_numpy_pytree(*, add: int = 0, include_scalars: bool = True):
  pytree = test_utils.setup_pytree(add=add)
  if include_scalars:
    pytree.update({'x': 4.5, 'y': 3})
  return pytree, jax.tree.map(as_abstract_type, pytree)

