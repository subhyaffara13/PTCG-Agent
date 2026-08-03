from typing import Any

def global_array_to_host_local_array(
    global_inputs: Any, global_mesh: jax.sharding.Mesh, pspecs: Any):
  r"""Converts a global `jax.Array` to a host local `jax.Array`.

  You can use this function to transition to `jax.Array`. Using `jax.Array` with
  pjit has the same semantics of using GDA with pjit i.e. all `jax.Array`
  inputs to pjit should be globally shaped and the output from pjit will also
  be globally shaped jax.Array's

  You can use this function to convert the globally shaped `jax.Array` output
  from pjit to host local values again so that the transition to jax.Array can
  be a mechanical change.

  Example usage:

  >>> from jax.experimental import multihost_utils # doctest: +SKIP
  >>>
  >>> global_inputs = multihost_utils.host_local_array_to_global_array(host_local_inputs, global_mesh, in_pspecs) # doctest: +SKIP
  >>>
  >>> with mesh: # doctest: +SKIP
  ...   global_out = pjitted_fun(global_inputs) # doctest: +SKIP
  >>>
  >>> host_local_output = multihost_utils.global_array_to_host_local_array(global_out, mesh, out_pspecs) # doctest: +SKIP

  Args:
    global_inputs: A Pytree of global jax.Array's.
    global_mesh: A :class:`jax.sharding.Mesh` object. The mesh must be contiguous
      meaning all local devices of the host must form a subcube.
    pspecs: A Pytree of :class:`jax.sharding.PartitionSpec` objects.

  Returns:
    A Pytree of host local arrays.
  """
  flat_inps, out_tree = tree_flatten(global_inputs)
  out_pspecs = _flatten_pspecs('output pspecs', out_tree,
                               pjit_lib.hashable_pytree(pspecs))
  out_flat = [
      global_array_to_host_local_array_p.bind(inp, global_mesh=global_mesh,
                                              pspec=o)
      for inp, o in safe_zip(flat_inps, out_pspecs)
  ]
  return tree_unflatten(out_tree, out_flat)


def global_array_to_host_local_array(out, cached, trace_state_clean):
  """Convert global arrays to host-local arrays for multihost pmap output.

  Args:
    out: The output pytree from jitted function.
    cached: CachedPmap tuple with mesh and sharding info.
    trace_state_clean: True if in execution mode (not tracing).

  Returns:
    Host-local output pytree.
  """
  if not trace_state_clean:
    import jax.experimental.multihost_utils as mhu  # pyrefly: ignore[missing-import]

    return mhu.global_array_to_host_local_array(
        out, cached.mesh, cached.out_specs
    )

  out_flat, out_tree = tree_flatten(out)
  out_local_shardings, out_global_shardings = _get_out_shardings(
      out_tree, cached.out_specs, cached.out_local_shardings_thunk
  )

  if out_flat and isinstance(out_flat[0], (core.Tracer, core.AbstractValue)):
    return out

  for i, arr in enumerate(out_flat):
    local_sharding = out_local_shardings[i]
    global_sharding = out_global_shardings[i]
    prng_impl = None
    typ = type(arr)
    if typ is array.ArrayImpl and arr.is_fully_addressable:
      continue
    if typ is not array.ArrayImpl:
      if typ is prng.PRNGKeyArray:
        prng_impl = arr.dtype._impl
        arr = arr._base_array
      try:
        _ = arr.shape
      except AttributeError:
        arr = np.array(arr)
      dtype = arr.dtype
      if dtype == dtypes.float0:
        arr = np.zeros(arr.shape, dtype=bool)
      if dtype != dtypes.canonicalize_dtype(dtype):
        arr = dtypes.canonicalize_value(arr)
    shape, dtype = arr.shape, arr.dtype
    typ = type(arr)

    local_aval = _global_to_local_aval(shape, dtype, global_sharding)
    if typ == array.ArrayImpl:
      if not _is_sharding_equivalent(arr.sharding, global_sharding, len(shape)):
        arr = api.device_put(arr, global_sharding)
      out_flat[i] = arr._rewrap_with_aval_and_sharding(
          local_aval, local_sharding
      )
    else:
      arrays = [
          arr[idx] for idx in _local_device_indices(local_sharding, shape)
      ]
      out_flat[i] = pxla.batched_device_put(
          local_aval,
          local_sharding,
          arrays,
          list(local_sharding._device_assignment),
      )
    if prng_impl is not None:
      out_flat[i] = prng.PRNGKeyArray(prng_impl, out_flat[i])

  return tree_unflatten(out_tree, out_flat)

