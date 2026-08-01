
def semaphore_signal_parallel(*signals: SemaphoreSignal):
  """Signals multiple semaphores without any guaranteed ordering of signal arrivals.

  This primitive is largely equivalent to::

    for sem in semaphores:
      pl.semaphore_signal(sem, inc, device_id=device_id)

  only unlike the loop above, it does not guarantee any ordering of signal
  arrivals. In particular, the target device might observe a signal on
  ``semaphores[1]`` before it observes a signal on ``semaphores[0]``.
  This operation still guarantees that any side effects performed before the
  signal will be fully performed and visible before any of the signals arrive.

  The relaxed requirements make the whole operation significantly cheaper on
  GPUs, as a single expensive memory fence can be used for all signals (instead
  of an expensive fence for each signal).
  """
  semaphores = [s.ref for s in signals]
  device_ids = [s.device_id for s in signals]
  incs = [jnp.asarray(s.inc, dtype=jnp.int32) for s in signals]
  refs, transforms = util.unzip2(
      map(pallas_primitives._get_ref_and_transforms, semaphores)
  )
  args = [refs, transforms, incs, device_ids]
  flat_args, args_tree = tree_util.tree_flatten(args)
  semaphore_signal_parallel_p.bind(
      *flat_args,
      args_tree=args_tree,
  )

