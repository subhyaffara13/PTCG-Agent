import functools

def truncate_array_and_mask(
    array: jax.Array,
    mask: jax.Array,
    edge_items_per_axis: tuple[int | None, ...],
) -> tuple[jax.Array, jax.Array]:
  """Truncates an array along the given axis names.

  Args:
    array: Array to truncate.
    mask: Mask array, which must have the same number of dimensions as `array`,
      and whose axis sizes must be either 1 or the same as that axis of `array`
      (e.g. they are broadcast compatible).
    edge_items_per_axis: Number of edge items to keep for each axis, ignoring
      any axes whose slices are already computed in `prefix_slices`.

  Returns:
    A tuple containing a truncated version of the array along with a valid mask.
    Values taken from the original array have the valid mask as True, and there
    is one extra element in the middle with valid as False (standing in for the
    omitted elements). The return value is always fully replicated, because
    we cannot guarantee that it is evenly sharded across devices, and this
    function is usually used immediately before copying to the host.
  """
  assert jax is not None, "JAX is not available."
  sharding_kwargs = {}
  if hasattr(array, "sharding") and hasattr(
      array.sharding, "_device_assignment"
  ):
    # _truncate_part_with_slices usually returns slices that have odd
    # dimensions, which aren't divisible by most shardings. Unfortunately,
    # the XLA GSPMD partitioner sometimes still infers a sharding over one of
    # these axes, which then leads to partitioning errors in JAX whenever we
    # try to `device_get` the resulting array or call any additional operations
    # on it. To avoid this, we'd like to tell JAX to always produce an output
    # that is not sharded over any axis. Unfortunately, this is difficult
    # because JAX requires the in_shardings and out_shardings to have the same
    # devices in the same internal order, and at the time of writing JAX does
    # not provide any public API to look up the order of the devices in a
    # sharding (it allows looking up the device *set*, but not their order).
    # Whether or not this error happens seems to be somewhat nondeterministic.
    # To avoid this, we use the private property `_device_assignment` of
    # each sharding in order to figure out what device order it has, and then
    # explicitly request a fully-replicated output that is definitely safe to
    # retrieve.
    sharding_kwargs["out_shardings"] = jax.sharding.NamedSharding(
        jax.sharding.Mesh(array.sharding._device_assignment, "x"),  # pylint: disable=protected-access
        jax.sharding.PartitionSpec(),
    )
  if array.size < SUMMARIZE_USING_NUMPY_THRESHOLD and safe_to_summarize(array):
    fn = functools.partial(_truncate_part_with_slices, xnp=np)
  else:
    fn = jax.jit(
        _truncate_part_with_slices, static_argnums=(2, 3), **sharding_kwargs
    )
  return fn(array, mask, (), edge_items_per_axis)

