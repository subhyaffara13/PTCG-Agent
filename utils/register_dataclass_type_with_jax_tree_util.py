import functools
import logging

def register_dataclass_type_with_jax_tree_util(data_class):
  """Register an existing dataclass so JAX knows how to handle it.

  This means that functions in jax.tree_util operate over the fields
  of the dataclass. See
  https://jax.readthedocs.io/en/latest/pytrees.html#extending-pytrees
  for further information.

  Args:
    data_class: A class created using dataclasses.dataclass. It must be
      constructable from keyword arguments corresponding to the members exposed
      in instance.__dict__.
  """
  def flatten(d):
    if d.__dict__:
      return tuple(zip(*sorted(d.__dict__.items())))[::-1]
    return ((), ())
  unflatten = functools.partial(_dataclass_unflatten, data_class)
  try:
    jax.tree_util.register_pytree_with_keys(
        nodetype=data_class, flatten_with_keys=_flatten_with_path,
        flatten_func=flatten, unflatten_func=unflatten)
  except ValueError:
    logging.info("%s is already registered as JAX PyTree node.", data_class)

