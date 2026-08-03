from typing import Any, Callable

def make_pjrt_c_api_client(
    plugin_name: str,
    options: OptionsDict | Callable[[], OptionsDict] | None = None,
) -> xla_client.Client:
  """Creates a PjRt client for the given plugin.

  Args:
    plugin_name: the name of the plugin.
    options: Optional. It is used when creating a PJRT plugin client. Can be a
      callable, in which case it will be invoked upon plugin initialization
      time, and will be expected to return an option dictionary.
  """
  if not xla_client.pjrt_plugin_initialized(plugin_name):
    xla_client.initialize_pjrt_plugin(plugin_name)
  updated_options: dict[str, Any] = {}
  if options is not None:
    updated_options.update(options() if callable(options) else options)
  updated_options.update(_options_from_jax_configs(plugin_name))
  if distributed.global_state.client is None:
    return xla_client.make_c_api_client(plugin_name, updated_options, None)

  distribute_options = {
      'node_id': distributed.global_state.process_id,
      'num_nodes': distributed.global_state.num_processes,
  }
  if (partition_index := distributed.global_state.partition_index) is not None:
    distribute_options['partition_index'] = partition_index
  if options is not None:
    distribute_options.update(updated_options)
  return xla_client.make_c_api_client(
      plugin_name,
      distribute_options,
      distributed.global_state.client,
      _make_transfer_server_factory(),
      FORCE_DCN_CROSS_HOST_TRANSFERS.value,
      SORT_DEVICES_BY_PROCESS_INDEX.value,
  )

