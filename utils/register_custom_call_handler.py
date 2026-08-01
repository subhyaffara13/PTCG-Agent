
def register_custom_call_handler(
    platform: str, handler: CustomCallHandler
) -> None:
  """Registers a custom handler and use it to register existing custom calls.

  If a custom call handler for the platform already exist, calling this method
  is a no-op and it will not register a new handler.

  Args:
    platform: the target platform.
    handler: the function to register a custom call.
  """
  xla_platform_name = xla_platform_names.get(platform, platform)
  with _custom_callback_lock:
    if xla_platform_name in _custom_callback_handler:
      logger.debug(
          'Custom call handler for %s is already register. Will not register a'
          ' new one',
          xla_platform_name,
      )
      return
    _custom_callback_handler[xla_platform_name] = handler
    if xla_platform_name in _custom_callback:
      for name, fn, api_version, traits in _custom_callback[xla_platform_name]:
        handler(name, fn, xla_platform_name, api_version, traits)
      del _custom_callback[xla_platform_name]

