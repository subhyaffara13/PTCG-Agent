
def _handle_array_process_allgather(inp, tiled):
  if isinstance(inp, array.ArrayImpl) and not inp.is_fully_addressable:
    if not tiled:
      raise ValueError(
          'Gathering global non-fully-addressable arrays only supports'
          ' tiled=True')
    if isinstance(inp.sharding, sharding_impls.NamedSharding):
      reps = inp.sharding.update(spec=P())
    else:
      reps = sharding_impls.GSPMDSharding.get_replicated(
          inp.sharding._device_assignment, memory_kind=inp.sharding.memory_kind)
    out = jax.jit(_identity_fn, out_shardings=reps)(inp)
  else:
    # All inputs here will be fully addressable.
    if jax.process_count() == 1:
      out = np.asarray(inp)
      return np.expand_dims(out, axis=0) if not tiled else out

    devices = np.array(jax.devices()).reshape(jax.process_count(),
                                              jax.local_device_count())
    global_mesh = jax.sharding.Mesh(devices, ('processes', 'local_devices'))
    pspec = P('processes')
    s = jax.sharding.NamedSharding(global_mesh, pspec)

    host_np_arr = np.asarray(inp)
    if host_np_arr.ndim == 0 or not tiled:
      host_np_arr = np.expand_dims(host_np_arr, axis=0)

    aval = core.ShapedArray(host_np_arr.shape, host_np_arr.dtype)
    pspec = sharding_impls.prepare_axis_resources(pspec, "pspec to array_mapping")
    global_aval = pxla.mesh_local_to_global(
        global_mesh, sharding_impls.get_array_mapping(pspec), aval)

    bufs = [jax.device_put(host_np_arr, d) for d in jax.local_devices()]
    global_arr = array.make_array_from_single_device_arrays(
        global_aval.shape, s, bufs)
    with jax.set_mesh(global_mesh):
      out = jax.jit(_identity_fn, out_shardings=P())(global_arr)
  return np.asarray(out.addressable_data(0))

