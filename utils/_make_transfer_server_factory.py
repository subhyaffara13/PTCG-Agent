
def _make_transfer_server_factory(
) -> _jax.TransferServerInterfaceFactory | None:
  """Creates a transfer server interface factory."""
  if (not CROSS_HOST_TRANSFER_SOCKET_ADDRESS.value or not
      hasattr(_jax, "make_transfer_server_interface_factory")):
    return None
  transport_addresses = []
  if CROSS_HOST_TRANSPORT_ADDRESSES.value:
    transport_addresses = CROSS_HOST_TRANSPORT_ADDRESSES.value.split(",")
  transfer_server_kwargs = {
      "distributed_client": distributed.global_state.client,
      "socket_address": CROSS_HOST_TRANSFER_SOCKET_ADDRESS.value,
      "transport_addresses": transport_addresses,
  }
  if CROSS_HOST_TRANSFER_TIMEOUT_SECONDS.value is not None:
    transfer_server_kwargs["cross_host_transfer_timeout_seconds"] = (
        CROSS_HOST_TRANSFER_TIMEOUT_SECONDS.value)
  if CROSS_HOST_TRANSFER_TRANSFER_SIZE.value is not None:
    transfer_server_kwargs["transfer_size"] = (
        CROSS_HOST_TRANSFER_TRANSFER_SIZE.value)
  return _jax.make_transfer_server_interface_factory(**transfer_server_kwargs)

