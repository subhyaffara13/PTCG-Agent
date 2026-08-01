
def _discover_and_register_pjrt_plugins():
  global _plugins_registered

  # Needs a separate lock because register_backend_factory (called from
  # register_plugin) requires to hold _backend_lock.
  with _plugin_lock:
    if not _plugins_registered:
      # Plugins in the namespace package `jax_plugins` or have an entry-point
      # under the `jax_plugins` group will be imported.
      discover_pjrt_plugins()
      # Registers plugins names and paths set in env var
      # PJRT_NAMES_AND_LIBRARY_PATHS, in the format of 'name1:path1,name2:path2'
      # ('name1;path1,name2;path2' for windows).
      register_pjrt_plugin_factories_from_env()
      with _plugin_callback_lock:
        for factory in _backend_factories.values():
          if factory.c_api is not None:
            for callback in _plugin_callbacks:
              callback(c_api=factory.c_api)
      _plugins_registered = True

