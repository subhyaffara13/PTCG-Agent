
def prefetch_to_device(
    iterator, size, devices=None, axis_name='_device_put_sharded'):
  """Shard and prefetch batches on device.

  This utility takes an iterator and returns a new iterator which fills an on
  device prefetch buffer. Eager prefetching can improve the performance of
  training loops significantly by overlapping compute and data transfer.

  This utility is mostly useful for GPUs, for TPUs and CPUs it should not be
  necessary -- the TPU & CPU memory allocators (normally) don't pick a memory
  location that isn't free yet so they don't block. Instead those allocators
  OOM.

  Args:
    iterator: an iterator that yields a pytree of ndarrays where the first
      dimension is sharded across devices.

    size: the size of the prefetch buffer.

      If you're training on GPUs, 2 is generally the best choice because this
      guarantees that you can overlap a training step on GPU with a data
      prefetch step on CPU.

    devices: the list of devices to which the arrays should be prefetched.

      Defaults to the order of devices expected by ``jax.pmap``.

    axis_name: the axis name to use for the prefetch.

  Yields:
    The original items from the iterator where each ndarray is now sharded to
    the specified devices.
  """
  queue = collections.deque()
  devices = _pmap_device_order() if devices is None else devices

  def _prefetch(xs):
    mesh = jax.sharding.Mesh(np.array(devices), (axis_name,))
    sharding = jax.NamedSharding(mesh, jax.P(axis_name))
    if isinstance(xs, jax.Array):
      return jax.device_put(jnp.stack(list(xs)), sharding)
    return jax.device_put(np.stack(list(xs)), sharding)

  def enqueue(n):  # Enqueues *up to* `n` elements from the iterator.
    for data in itertools.islice(iterator, n):
      queue.append(jax.tree_util.tree_map(_prefetch, data))

  enqueue(size)  # Fill up the buffer.
  while queue:
    yield queue.popleft()
    enqueue(1)

