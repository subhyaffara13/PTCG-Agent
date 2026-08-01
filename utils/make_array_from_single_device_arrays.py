
def make_array_from_single_device_arrays(
    shape: Shape, sharding: Sharding, arrays: Sequence[basearray.Array], *,
    dtype: DTypeLike | None = None,
) -> ArrayImpl:
  r"""Returns a ``jax.Array`` from a sequence of ``jax.Array``\s each on a single device.
      Every device in input ``sharding``\'s mesh must have an array in ``arrays``\s.

  Args:
    shape : Shape of the output ``jax.Array``. This conveys information already included with
      ``sharding`` and ``arrays`` and serves as a double check.
    sharding: Sharding: A global Sharding instance which describes how the output jax.Array is laid out across devices.
    arrays: `list` or `tuple` of ``jax.Array``\s that are each single device addressable. ``len(arrays)``
      must equal ``len(sharding.addressable_devices)`` and the shape of each array must be the same. For multiprocess code,
      each process will call with a different ``arrays`` argument that corresponds to that processes' data.
      These arrays are commonly created via ``jax.device_put``.
    dtype: The dtype of the output ``jax.Array``. If not provided, the dtype of the first array in
      ``arrays`` is used. If ``arrays`` is empty, the ``dtype`` argument must be provided.

  Returns:
    A global ``jax.Array``, sharded as ``sharding``, with shape equal to ``shape``, and with per-device
      contents matching ``arrays``.

  Examples:

    >>> import math
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> mesh_rows = 2
    >>> mesh_cols =  jax.device_count() // 2
    ...
    >>> global_shape = (8, 8)
    >>> mesh = Mesh(np.array(jax.devices()).reshape(mesh_rows, mesh_cols), ('x', 'y'))
    >>> sharding = jax.sharding.NamedSharding(mesh, P('x', 'y'))
    >>> inp_data = np.arange(math.prod(global_shape)).reshape(global_shape)
    ...
    >>> arrays = [
    ...    jax.device_put(inp_data[index], d)
    ...        for d, index in sharding.addressable_devices_indices_map(global_shape).items()]
    ...
    >>> arr = jax.make_array_from_single_device_arrays(global_shape, sharding, arrays)
    >>> assert arr.shape == (8,8) # arr.shape is (8,8) regardless of jax.device_count()

  For cases where you have a local array and want to convert it to a global
  jax.Array, use ``jax.make_array_from_process_local_data``.
  """
  if isinstance(arrays, Sequence):
    dtype = _get_and_check_dtype(
        arrays, dtype, "make_array_from_single_device_arrays")

  # All input arrays should be committed. Checking it is expensive on
  # single-controller systems.
  aval = core.update_aval_with_sharding(
      core.ShapedArray(shape, dtype, weak_type=False), sharding)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    return aval.dtype._rules.make_sharded_array(aval, sharding, arrays,
                                                committed=True)
  arrays = list(arrays) if isinstance(arrays, tuple) else arrays
  # TODO(phawkins): ideally the cast() could be checked.
  try:
    return ArrayImpl(aval, sharding, cast(Sequence[ArrayImpl], arrays),
                     committed=True)
  except TypeError:
    if not isinstance(arrays, list):
      raise TypeError("jax.make_array_from_single_device_arrays `arrays` "
                      "argument must be a list or tuple, but got "
                      f"{type(arrays)}.")
    if any(isinstance(arr, core.Tracer) for arr in arrays):
      raise ValueError(
          "jax.make_array_from_single_device_arrays requires a list of concrete"
          f" arrays as input, but got types {set(map(type, arrays))}")
    raise

