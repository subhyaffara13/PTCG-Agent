
def _device_put_sharding_impl(
    x: Any,
    aval: core.ShapedArray,
    device: Device | Sharding | None,
    copy: ArrayCopySemantics,
):
  from jax.experimental import multihost_utils  # pyrefly: ignore[missing-import]

  # Use a dynamic type, because the static type depends on the value of
  # ``x_is_jax_array``.
  x_sharding: Any
  if isinstance(x, array.ArrayImpl):
    x_is_jax_array = True
    x_is_fully_addressable, x_sharding = x.is_fully_addressable, x.sharding
  else:
    x_is_jax_array = False
    x_is_fully_addressable, x_sharding = None, None

  if isinstance(device, Sharding):
    s = device
    s_is_fully_addressable = s.is_fully_addressable
    if (getattr(x, 'sharding', None) == s and getattr(x, '_committed', False)
        and copy == ArrayCopySemantics.REUSE_INPUT):
      return x

    if isinstance(s, NamedSharding) and s.spec.unreduced:
      # TODO(mattjj,yashkatariya): handle donation
      return api.jit(_device_put_reshard, out_shardings=s)(x)

    if (not s_is_fully_addressable and
        x_is_jax_array and not x_is_fully_addressable and
        s.device_set == x_sharding.device_set):
      assert isinstance(s, NamedSharding), s
      return _different_device_order_reshard(x, s, copy)

    if (s_is_fully_addressable and x_is_jax_array and
        x_is_fully_addressable and s.num_devices > 1 and
        s._internal_device_list != x_sharding._internal_device_list and
        s.device_set == x_sharding.device_set):
      assert isinstance(s, NamedSharding), s
      return _different_device_order_reshard(x, s, copy)

    if (x_is_jax_array and x._committed and xla_bridge.process_count() > 1
        and _is_supported_cross_host_transfer(x.ndim, x_sharding, s)):
      return _DeferredCrossHostTransferArg(x, s, copy)

    if not s_is_fully_addressable:
      # If both the source and target shardings are not fully addressable and
      # one of the above conditions has not been met, then assume that the user
      # is attempting a different device order reshard.
      if (x_is_jax_array and not x_is_fully_addressable
          and s.device_set != x_sharding.device_set):
        inp_ids = [d.id for d in x_sharding._device_assignment]
        inp_plat = x_sharding._device_assignment[0].platform.upper()
        target_ids = [d.id for d in s._device_assignment]
        target_plat = s._device_assignment[0].platform.upper()
        raise ValueError(
            "For a cross-host reshard in multi-controller JAX, input and target"
            " sharding should have the same set of devices. Got input's device"
            f" set ids: {inp_ids} on platform {inp_plat} and target sharding's"
            f" device set ids: {target_ids} on platform {target_plat}.\n\n"
            "There is experimental support for cross-host transfers with "
            "different device sets, when input/output shardings have the same "
            "indices and layouts, in the TFRT TPU runtime only.")

      if ((x_is_jax_array and not x._committed) or
          type(x) in array_types or type(x) in dtypes.python_scalar_types):
        # If all hosts participate in the sharding, assert that the input is the
        # same on all hosts. If some hosts have no addressable devices in the
        # sharding, bypass the check, since we can't easily distinguish between
        # these two cases: (1) the sharding contains the same subset of global
        # devices on all hosts (and hosts with no addressable devices in the
        # sharding do not transfer data) or (2) the sharding contains a
        # different subset of devices on each host. For (1), the input should be
        # the same on all hosts, but for (2) it need not be.
        if xla_bridge.process_count() == len(s._internal_device_list.process_indices):
          multihost_utils.assert_equal(
              x, fail_message=(
                  f"{type(x)} passed to device_put is not the same on each"
                  " process. Make sure you are passing the same value of"
                  f" {type(x)} on each process."))
        return _DeferredShardArg(x, s, aval, True, copy)
      # TODO(yashkatariya,mattjj): Link to a doc about McJAX and jax.Array.
      raise ValueError(
          "device_put's second argument must be a Device or a Sharding which"
          f" represents addressable devices, but got {s}. Please pass device or"
          " Sharding which represents addressable devices.")
    return _DeferredShardArg(x, s, aval, True, copy)

  # Only `Device` exists below. `Sharding` instance is handled above.
  if x_is_jax_array:
    if not x_is_fully_addressable and not x_sharding.num_devices == 1:
      raise ValueError(
          "When the second argument to `device_put` is a Device, the first "
          "argument must be a fully addressable array or a non-addressable "
          "array with a single device sharding. Got value with devices "
          f"{x.devices()}")
    if device is None:
      if copy == ArrayCopySemantics.REUSE_INPUT:
        return x
      else:
        return _DeferredShardArg(x, x_sharding, aval, x.committed, copy)
    elif x_sharding.num_devices == 1:
      device = x_sharding._device_assignment[0] if device is None else device
      sharding = make_single_device_sharding(device)
      if not x._committed and not sharding.has_addressable_devices:
        # For uncommitted arrays in McJAX, each process has a local copy of the
        # array. If the destination sharding is not addressable, no data
        # transfer is needed, since the data was transferred in the process
        # in which the sharding is addressable.
        shards, devices = [], []
      else:
        shards, devices = [x], [device]
      if copy == ArrayCopySemantics.ALWAYS_COPY:
        return xc.batched_device_put(aval, sharding, shards, devices, True,
                                     True)
      return pxla.batched_device_put(aval, sharding, shards, devices)

  sh = make_single_device_sharding(pxla.get_default_device()
                                   if device is None else device)
  return _DeferredShardArg(x, sh, aval, device is not None, copy)

