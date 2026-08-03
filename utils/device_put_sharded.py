from typing import Any

def device_put_sharded(shards: Sequence[Any], devices: Sequence[xc.Device]):  # noqa: F811
  """Transfer array shards to specified devices and form Array(s).

  Args:
    shards: A sequence of arrays, scalars, or (nested) standard Python
      containers thereof representing the shards to be stacked together to form
      the output. The length of ``shards`` must equal the length of ``devices``.
    devices: A sequence of :py:class:`Device` instances representing the devices
      to which corresponding shards in ``shards`` will be transferred.

  This function is always asynchronous, i.e. returns immediately.

  Returns:
    A Array or (nested) Python container thereof representing the
    elements of ``shards`` stacked together, with each shard backed by physical
    device memory specified by the corresponding entry in ``devices``.

  Examples:
    Passing a list of arrays for ``shards`` results in a sharded array
    containing a stacked version of the inputs:

    >>> import jax
    >>> devices = jax.local_devices()
    >>> x = [jax.numpy.ones(5) for device in devices]
    >>> y = jax.device_put_sharded(x, devices)  # doctest: +SKIP
    >>> np.allclose(y, jax.numpy.stack(x))  # doctest: +SKIP
    True

    Passing a list of nested container objects with arrays at the leaves for
    ``shards`` corresponds to stacking the shards at each leaf. This requires
    all entries in the list to have the same tree structure:

    >>> x = [(i, jax.numpy.arange(i, i + 4)) for i in range(len(devices))]
    >>> y = jax.device_put_sharded(x, devices)  # doctest: +SKIP
    >>> type(y)  # doctest: +SKIP
    <class 'tuple'>
    >>> y0 = jax.device_put_sharded([a for a, b in x], devices)  # doctest: +SKIP
    >>> y1 = jax.device_put_sharded([b for a, b in x], devices)  # doctest: +SKIP
    >>> np.allclose(y[0], y0)  # doctest: +SKIP
    True
    >>> np.allclose(y[1], y1)  # doctest: +SKIP
    True

  See Also:
    - device_put
    - device_put_replicated
  """
  # TODO(jakevdp): provide a default for devices that considers both local
  # devices and pods
  if not isinstance(shards, Sequence):
    raise TypeError("device_put_sharded `shards` input must be a sequence; "
                     f"got {type(shards)}")
  if len(shards) != len(devices):
    raise ValueError(f"len(shards) = {len(shards)} must equal "
                     f"len(devices) = {len(devices)}.")

  def _device_put_sharded(*xs):
    avals = [core.typeof(x) for x in xs]
    if not all(a1 == a2 for a1, a2 in zip(avals[:-1], avals[1:])):
      a1, a2 = next((a1, a2) for a1, a2 in zip(avals[:-1], avals[1:])
                    if a1 != a2)
      raise ValueError("the shards passed to device_put_sharded must have "
                       f"consistent shape and dtype, but got {a1} and {a2}.")
    stacked_aval = avals[0].update(shape=(len(devices),) + avals[0].shape)
    mesh = Mesh(np.array(devices), ("_device_put_sharded",))
    sharding = NamedSharding(mesh, P("_device_put_sharded"))
    if dtypes.issubdtype(stacked_aval.dtype, dtypes.extended):
      return stacked_aval.dtype._rules.device_put_sharded(xs, stacked_aval, sharding, devices)
    ys = []
    for x in xs:
      if not isinstance(x, (np.ndarray, basearray.Array)):
        x = np.asarray(x)
      ys.append(x[None])
    return pxla.batched_device_put(stacked_aval, sharding, ys, list(devices))


  with config.explicit_device_put_scope():
    return tree_map(_device_put_sharded, *shards)

