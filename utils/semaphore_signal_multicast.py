
def semaphore_signal_multicast(
    semaphore,
    value: int | jax.Array = 1,
    *,
    collective_axes: Hashable | tuple[Hashable, ...],
):
  """Signals a semaphore on all devices along collective_axes.

  At the moment only signals to all devices are supported.

  Args:
    semaphore: The semaphore reference to signal.
    value: The increment value for the semaphore.
    collective_axes: The mesh axes to multicast the signal across.
      Must contain all mesh axes.
  """
  if not isinstance(collective_axes, tuple):
    collective_axes = (collective_axes,)
  ref, transforms = pallas_primitives._get_ref_and_transforms(semaphore)
  value = jnp.asarray(value, dtype=jnp.int32)
  args = [ref, transforms, value]
  flat_args, args_tree = tree_util.tree_flatten(args)
  return semaphore_signal_multicast_p.bind(
      *flat_args,
      args_tree=args_tree,
      collective_axes=collective_axes,
  )

