
def _is_supported_cross_host_transfer(ndim, src_sharding, dst_sharding):
  """Returns True if src->dst is a supported cross-host transfer."""
  if (src_sharding._internal_device_list.device_kind !=
      dst_sharding._internal_device_list.device_kind):
    return False
  if (src_sharding._to_xla_hlo_sharding(ndim) !=
      dst_sharding._to_xla_hlo_sharding(ndim)):
    return False
  # This check excludes the case where the source and destination shardings
  # have the same process index sets but there are shards that require
  # cross-host transfers. This case is supportable but expensive to check for.
  different_process_inds = (
      src_sharding._internal_device_list.process_indices !=
      dst_sharding._internal_device_list.process_indices)
  backend = xla_bridge.get_backend()
  # If a cross-host device transfer is requested but the backend does not
  # support it, then the user must set the flags to enable DCN-based transfers.
  if (different_process_inds and
      (xla_bridge.FORCE_DCN_CROSS_HOST_TRANSFERS.value
      or not getattr(backend, "supports_cross_host_transfers", False)) and
      not xla_bridge.CROSS_HOST_TRANSFER_SOCKET_ADDRESS.value):
    if xla_bridge.FORCE_DCN_CROSS_HOST_TRANSFERS.value:
      msg = ("DCN-based cross-host transfers were requested with the "
             "jax_force_dcn_cross_host_transfers flag.")
    else:
      msg = ("The backend ({backend.platform}, {backend.platform_version}) "
             "does not support cross-host device transfers.")
    raise ValueError(
        f"{msg} Please set jax_cross_host_transfer_socket_address and "
        "(optionally) jax_cross_host_transport_addresses flags to enable "
        "DCN-based cross host device transfers.")
  return different_process_inds

