from typing import Callable

def make_array_from_callback(
    shape: Shape, sharding: Sharding | Format,
    data_callback: Callable[[Index | None], ArrayLike],
    dtype: DTypeLike | None = None) -> ArrayImpl:
  # pyformat: disable
  """Returns a ``jax.Array`` via data fetched from ``data_callback``.

  ``data_callback`` is used to fetch the data for each addressable shard of the
  returned ``jax.Array``. This function must return concrete arrays, meaning that
  ``make_array_from_callback`` has limited compatibility with JAX transformations
  like :func:`jit` or :func:`vmap`.

  Args:
    shape : Shape of the ``jax.Array``.
    sharding: A ``Sharding`` instance which describes how the ``jax.Array`` is
      laid out across devices.
    data_callback : Callback that takes indices into the global array value as
      input and returns the corresponding data of the global array value.
      The data can be returned as any array-like object, e.g. a ``numpy.ndarray``.
    dtype: The dtype of the output ``jax.Array``. If not provided, the dtype of
      the data for the first addressable shard is used. If there are no
      addressable shards, the ``dtype`` argument must be provided.

  Returns:
    A ``jax.Array`` via data fetched from ``data_callback``.

  Examples:

    >>> import math
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> input_shape = (8, 8)
    >>> global_input_data = np.arange(math.prod(input_shape)).reshape(input_shape)
    >>> global_mesh = Mesh(np.array(jax.devices()).reshape(2, 4), ('x', 'y'))
    >>> inp_sharding = jax.sharding.NamedSharding(global_mesh, P('x', 'y'))
    ...
    >>> def cb(index):
    ...  return global_input_data[index]
    ...
    >>> arr = jax.make_array_from_callback(input_shape, inp_sharding, cb)
    >>> arr.addressable_data(0).shape
    (4, 2)
  """
  # pyformat: enable
  dll = sharding.layout if isinstance(sharding, Format) else None
  if isinstance(dll, AutoLayoutSingleton):
    raise TypeError(
        "`Layout.AUTO` cannot be used in place of a device-local"
        f" layout when calling `jax.make_array_from_callback`. Got {sharding}")
  processed_sharding = sharding.sharding if isinstance(sharding, Format) else sharding
  if not isinstance(processed_sharding, Sharding):
    raise TypeError(
        f"sharding should be an instance of `jax.sharding`. Got {processed_sharding} of"
        f" type {type(processed_sharding)}")
  sharding = processed_sharding

  def get_data(
      index: Index | None,
  ) -> ArrayImpl | literals.TypedNdArray | np.ndarray:
    # Perhaps cache on index here, then we can unify fully_replicated
    # and non-fully_replicated cases below and become faster for
    # partially replicated cases.
    assert index is not None
    r = data_callback(index)
    if isinstance(r, core.Tracer):
      raise errors.UnexpectedTracerError(
          "jax.make_array_from_callback cannot be called within a traced"
          " context."
      )
    # Value can be python scalars, resolve it into something with dtype.
    r = dtypes.canonicalize_value(r)
    if isinstance(r, (literals.TypedInt, literals.TypedFloat,
                      literals.TypedComplex)):
      r = literals.TypedNdArray(np.asarray(r, dtype=r.dtype))
    elif isinstance(r, bool):
      r = literals.TypedNdArray(np.asarray(r, dtype=np.bool_))
    return r

  if sharding.is_fully_replicated:
    devices = list(sharding._internal_device_list.addressable_device_list)
    # Only compute data once.
    per_device_values = [get_data((slice(None),) * len(shape))] * len(devices)
  else:
    device_to_index_map = sharding.addressable_devices_indices_map(shape)
    devices = list(device_to_index_map.keys())
    per_device_values = [
        get_data(device_to_index_map[device]) for device in devices
    ]

  dtype = _get_and_check_dtype(
      per_device_values, dtype, "make_array_from_callback")
  expected_shape = sharding.shard_shape(shape)
  aval = core.update_aval_with_sharding(
      core.ShapedArray(shape, dtype), sharding)

  _validate_shape_and_dtype_for_per_device_arrays(
      per_device_values,
      expected_shape=expected_shape,
      aval=aval,
      sharding=sharding,
  )
  first_value = None
  if per_device_values:
    first_value = per_device_values[0]
    if (isinstance(first_value, ArrayImpl)
        and first_value._committed
        and sharding.is_fully_replicated
        and first_value.is_fully_replicated
        and first_value.sharding._device_assignment == tuple(devices)
        and first_value.format.layout == dll):
      return first_value

  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    # TODO(yashkatariya): Can this also use batched_device_put?
    arrays = api.device_put(per_device_values, devices)
    return aval.dtype._rules.make_sharded_array(
        aval, sharding, arrays, committed=True
    )

  if dll is not None:
    devices = [Format(dll, make_single_device_sharding(d)) for d in devices]
    # pxla.batched_device_put doesn't support Layout... Take the slow route
    arrays = api.device_put(per_device_values, devices)
    return ArrayImpl(aval, sharding, arrays, committed=True)

  if isinstance(first_value, ArrayImpl) and len(first_value.devices()) > 1:
    # The output of the callback is already a sharded array, move it to
    # to target device.
    per_device_values = api.device_put(per_device_values, devices)

  return pxla.batched_device_put(aval, sharding, per_device_values, devices)

