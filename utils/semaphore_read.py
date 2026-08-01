
def semaphore_read(sem_or_view) -> jax_typing.Array:
  """Reads the value of a semaphore.

  Args:
    sem_or_view: A Ref (or view) representing a semaphore.

  Returns:
    A scalar Array containing the value of the semaphore.
  """
  ref, transforms = _get_ref_and_transforms(sem_or_view)
  args = [ref, transforms]
  flat_args, args_tree = tree_util.tree_flatten(args)
  return semaphore_read_p.bind(*flat_args, args_tree=args_tree)

