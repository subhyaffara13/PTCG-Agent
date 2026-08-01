
def register_plugin(
    plugin_name: str,
    *,
    priority: int = 400,
    library_path: str | None = None,
    options: OptionsDict | Callable[[], OptionsDict] | None = None,
    c_api: Any | None = None,
    factory: BackendFactory | None = None,
    make_topology: TopologyFactory | None = None,
) -> Any:
  """Registers a backend factory for the PJRT plugin.

  Args:
    plugin_name: the name of the plugin.
    priority: the priority this plugin should be registered in jax backends.
      Default to be 400.
    library_path: Optional. The full path to the .so file of the plugin. The
      plugin needs to provide either the library_path or the c_api.
    options: Optional. It is used when creating a PJRT plugin client. Can be a
      callable, in which case it will be invoked upon plugin initialization
      time, and will be expected to return an option dictionary.
    c_api: Optional. The plugin can provide a PJRT C API to be registered.
    factory: Optional. A factory function that creates a PJRT client. If not
      provided, a default factory will be used.
  """

  if library_path and c_api:
    logger.error(
        "Both library_path and c_api are provided when registering PJRT plugin"
        " %s",
        plugin_name,
    )
    return
  if not library_path and not c_api:
    logger.error(
        "Neither library_path nor c_api provided when registering PJRT plugin"
        " %s",
        plugin_name,
    )
    return

  if factory is not None and options is not None:
    raise ValueError(
        "Cannot provide both 'factory' and 'options' when registering PJRT"
        " plugin. When providing a custom factory, the factory's must handle"
        " its own options."
    )
  if factory is None:
    factory = partial(make_pjrt_c_api_client, plugin_name, options=options)

  logger.debug(
      'registering PJRT plugin %s from %s', plugin_name, library_path
  )
  if library_path is not None:
    c_api = xla_client.load_pjrt_plugin_dynamically(plugin_name, library_path)
    _profiler.register_plugin_profiler(c_api)
  else:
    assert c_api is not None
    xla_client.load_pjrt_plugin_with_c_api(plugin_name, c_api)

  make_topology = make_topology or partial(xla_client.make_c_api_device_topology, c_api)
  experimental = plugin_name not in _nonexperimental_plugins
  register_backend_factory(plugin_name, factory, priority=priority,
                           fail_quietly=False, experimental=experimental,
                           make_topology=make_topology, c_api=c_api)
  return c_api

