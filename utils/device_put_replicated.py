from typing import Any

def device_put_replicated(x: Any, devices: Sequence[xc.Device]):  # noqa: F811
  """Transfer array(s) to each specified device and form Array(s).

  Args:
    x: an array, scalar, or (nested) standard Python container thereof
      representing the array to be replicated to form the output.
    devices: A sequence of :py:class:`Device` instances representing the devices
      to which ``x`` will be transferred.

  This function is always asynchronous, i.e. returns immediately.

  Returns:
    An Array or (nested) Python container thereof representing the
    value of ``x`` broadcasted along a new leading axis of size
    ``len(devices)``, with each slice along that new leading axis backed by
    memory on the device specified by the corresponding entry in ``devices``.

  Examples:
    Passing an array:

    >>> import jax
    >>> devices = jax.local_devices()
    >>> x = jax.numpy.array([1., 2., 3.])
    >>> y = jax.device_put_replicated(x, devices)  # doctest: +SKIP
    >>> np.allclose(y, jax.numpy.stack([x for _ in devices]))  # doctest: +SKIP
    True

  See Also:
    - device_put
    - device_put_sharded
  """
  if not isinstance(devices, Sequence) or not devices:
    raise ValueError("`devices` argument to `device_put_replicated must be "
                     "a non-empty sequence.")
  def _device_put_replicated(x):
    aval = core.unmapped_aval(len(devices), 0, core.typeof(x))
    assert isinstance(aval, ShapedArray)
    if isinstance(x, (np.ndarray, basearray.Array)):
      buf = device_put(x[None], devices[0])
    else:
      buf = device_put(x, devices[0])[None]
    mesh = Mesh(np.array(devices), ("_device_put_replicated",))
    sharding = NamedSharding(mesh, P("_device_put_replicated"))
    if dtypes.issubdtype(aval.dtype, dtypes.extended):
      return aval.dtype._rules.device_put_replicated(buf, aval, sharding, devices)
    return pxla.batched_device_put(aval, sharding, [buf] * len(devices), devices)

  with config.explicit_device_put_scope():
    return tree_map(_device_put_replicated, x)

