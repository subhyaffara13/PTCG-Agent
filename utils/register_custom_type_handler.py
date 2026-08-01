
def register_custom_type_handler(
    platform: str, handler: CustomTypeIdHandler
) -> None:
  """Register a custom type id handler and use it to register existing type ids.

  If a custom type id handler for the platform already exist, calling this
  method is a no-op and it will not register a new handler.

  Args:
    platform: the target platform.
    handler: the function to register a custom type id.
  """
  xla_platform_name = xla_platform_names.get(platform, platform)
  with _custom_callback_lock:
    if xla_platform_name in _custom_type_id_handler:
      logger.debug(
          'Custom type id handler for %s is already register. Will not '
          'register a new one',
          xla_platform_name,
      )
      return
    _custom_type_id_handler[xla_platform_name] = handler
    if xla_platform_name in _custom_type_id:
      for name, capsule in _custom_type_id[xla_platform_name]:
        handler(name, capsule)
      del _custom_type_id[xla_platform_name]

