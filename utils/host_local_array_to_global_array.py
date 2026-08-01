
def host_local_array_to_global_array(
    local_inputs: Any, global_mesh: jax.sharding.Mesh, pspecs: Any):
  r"""Converts a host local value to a globally sharded jax.Array.

  This function takes host-local data (which might be different
  across hosts), and populates a global array with this data, where each
  device on each host, get the appropriate slice of the data according to
  sharding defined by the global_mesh/pspects.

  For example:

  >>> global_mesh = jax.sharding.Mesh(jax.devices(), 'x')
  >>> pspecs = jax.sharding.PartitionSpec('x')
  >>> host_id = jax.process_index()
  >>> arr = host_local_array_to_global_array(np.arange(4) * host_id, mesh, pspecs)  # NB: assumes jax.local_device_count() divides 4.   # doctest: +SKIP

  The resulting array will have the shape (4 * num_processes) and will
  have distributed value of: (0, 1, 2, 3, 0, 2, 4, 6, 0, 3, 6, 9, ... ),
  where each slice np.arange(4) * host_id will be partitioned across the
  corresponding host's devices.

  Similarly:

  >>> mesh = jax.sharding.Mesh(np.array(jax.devices()).reshape(jax.process_count(), jax.local_device_count()), ['host', 'dev'])
  >>> pspecs = jax.sharding.PartitionSpec('host')
  >>> host_id = jax.process_index()
  >>> arr = host_local_array_to_global_array(np.arange(4) * host_id, mesh, pspecs)  # doctest: +SKIP

  will create the same distributed value (0, 1, 2, 3, 0, 2, 4, 6, ...),
  however each slice np.arange(4) * i will be *replicated* across corresponding
  host devices.

  On the other hand, if pspecs = PartitionSpec(), which means
  replication across all axes, then this snippet:

  >>> pspecs = jax.sharding.PartitionSpec()
  >>> arr = host_local_array_to_global_array(np.arange(4), mesh, pspecs)  # doctest: +SKIP

  will have the shape (4,) and the value (0, 1, 2, 3) will be replicated
  across all hosts and devices.

  It is an undefined behavior to have not identical local_inputs with pspec
  indicating data replication.

  You can use this function to transition to jax.Array. Using jax.Array with
  pjit has the same semantics of using GDA with pjit i.e. all jax.Array
  inputs to pjit should be globally shaped.

  If you are currently passing host local values to pjit, you can use this
  function to convert your host local values to global Arrays and then pass that
  to pjit.


  Example usage.

  >>> from jax.experimental import multihost_utils # doctest: +SKIP
  >>>
  >>> global_inputs = multihost_utils.host_local_array_to_global_array(host_local_inputs, global_mesh, in_pspecs) # doctest: +SKIP
  >>>
  >>> with mesh: # doctest: +SKIP
  >>>   global_out = pjitted_fun(global_inputs) # doctest: +SKIP
  >>>
  >>> host_local_output = multihost_utils.global_array_to_host_local_array(global_out, mesh, out_pspecs) # doctest: +SKIP

  Please note this function requires global mesh to be a continuous mesh, meaning
  that  devices that belong to each host should form a subcube in this mesh.
  To move local data to global array with non-continuous mesh use
  jax.make_array_from_callback or jax.make_array_from_single_device_arrays
  instead.

  Args:
    local_inputs: A Pytree of host local values.
    global_mesh: A jax.sharding.Mesh object. The mesh must be a contiguous mesh,
    that is all hosts' devices must form a subcube in this mesh.
    pspecs: A Pytree of jax.sharding.PartitionSpec's.

  Returns:
    A pytree of global arrays.
  """
  flat_inps, in_tree = tree_flatten(local_inputs)
  in_pspecs = _flatten_pspecs('input pspecs', in_tree,
                              pjit_lib.hashable_pytree(pspecs))
  out_flat = [
      host_local_array_to_global_array_p.bind(inp, global_mesh=global_mesh,
                                              pspec=in_spec)
      for inp, in_spec in safe_zip(flat_inps, in_pspecs)
  ]
  return tree_unflatten(in_tree, out_flat)


def host_local_array_to_global_array(
    dyn_args_flat, cached, trace_state_clean, donated_invars
):
  """Convert host-local arrays to global arrays for multihost pmap.

  Args:
    dyn_args_flat: Flat list of input arrays.
    cached: CachedPmap tuple with mesh and sharding info.
    trace_state_clean: True if in execution mode (not tracing).
    donated_invars: Tuple of bools indicating which args are donated. For
      donated args that require the slow path, we delete the original to free
      memory.

  Returns:
    Converted global arrays.
  """
  if not trace_state_clean:
    import jax.experimental.multihost_utils as mhu  # pyrefly: ignore[missing-import]

    return list(
        mhu.host_local_array_to_global_array(
            tuple(dyn_args_flat), cached.mesh, cached.in_specs_flat
        )
    )

  in_local_shardings = cached.in_local_shardings
  in_global_shardings = cached.in_global_shardings

  if dyn_args_flat and isinstance(
      dyn_args_flat[0], (core.Tracer, core.AbstractValue)
  ):
    return dyn_args_flat

  for i, arr in enumerate(dyn_args_flat):
    local_sharding = in_local_shardings[i]
    global_sharding = in_global_shardings[i]
    donated = donated_invars[i]
    prng_impl = None
    typ = type(arr)
    if typ is array.ArrayImpl and not arr.is_fully_addressable:
      continue
    if typ is not array.ArrayImpl:
      if typ is prng.PRNGKeyArray:
        prng_impl = arr.dtype._impl
        arr = arr._base_array
      arr = np.asarray(arr)
      dtype = arr.dtype
      if dtype == dtypes.float0:
        arr = np.zeros(arr.shape, dtype=bool)
      if dtype != dtypes.canonicalize_dtype(dtype):
        arr = dtypes.canonicalize_value(arr)
    shape, dtype = arr.shape, arr.dtype
    typ = type(arr)

    global_aval = _local_to_global_aval(shape, dtype, global_sharding)
    if typ == array.ArrayImpl and _is_sharding_equivalent(
        arr.sharding, local_sharding, len(arr.shape)
    ):
      # Fast path: rewrap without copy (shares buffers with original).
      # For donated args, jit's donation will invalidate the shared buffers,
      # which is the expected behavior - original arrays become invalid.
      dyn_args_flat[i] = arr._rewrap_with_aval_and_sharding(
          global_aval, global_sharding
      )
    else:
      # Slow path: slice and device_put (creates new buffers).
      # For donated args, we must explicitly delete the original to free memory.
      arrays = [
          arr[idx] for idx in _local_device_indices(local_sharding, shape)
      ]
      dyn_args_flat[i] = pxla.batched_device_put(
          global_aval,
          global_sharding,
          arrays,
          list(local_sharding._device_assignment),
      )
      if donated and typ is array.ArrayImpl:
        warnings.warn(
            "Donated pmap argument required resharding. This causes a brief "
            "2x memory spike before the original is freed. For optimal "
            "donation, ensure inputs are correctly sharded before pmap.",
            stacklevel=4,
        )
        arr.delete()
    if prng_impl is not None:
      dyn_args_flat[i] = prng.PRNGKeyArray(prng_impl, dyn_args_flat[i])

  return dyn_args_flat

