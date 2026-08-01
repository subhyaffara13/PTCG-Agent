
def make_c_api_client(
    plugin_name: str,
    options: _NameValueMapping | None = None,
    distributed_client: _xla.DistributedRuntimeClient | None = None,
    transfer_server_factory: _xla.TransferServerInterfaceFactory | None = None,
    force_dcn_cross_host_transfers: bool = False,
    sort_devices_by_process_index: bool = True,
):
  """Creates a PJRT C API client for a PJRT plugin.

  It is required that load_pjrt_plugin_dynamically is called once with the same
  plugin_name before this method is called.

  Args:
     plugin_name: the name of the PJRT plugin.
     options: extra platform-specific options.
     distributed_client: distributed client.

  Returns:
     A PJRT C API client for plugin_name.
  """
  if options is None:
    options = {}
  return _xla.get_c_api_client(
      plugin_name,
      options,
      distributed_client,
      transfer_server_factory,
      force_dcn_cross_host_transfers,
      sort_devices_by_process_index,
  )

