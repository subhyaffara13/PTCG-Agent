
def register_plugin_callbacks(callback):
  """Registers a callback to be called with c_api after plugins discovery.

  The callback will be called on all discovered PJRT C API plugins. If
  `register_plugin_callbacks` is called before the plugins are discovered, the
  callback will be called right after the plugins are discovered. Otherwise, the
  callback will be called immediately when `register_plugin_callbacks` is
  called.

  Args:
    callback: the callback to be called with c_api.
  """
  with _plugin_callback_lock:
    if _plugins_registered:
      for factory in _backend_factories.values():
        if factory.c_api is not None:
          callback(c_api=factory.c_api)
    else:
      _plugin_callbacks.append(callback)

