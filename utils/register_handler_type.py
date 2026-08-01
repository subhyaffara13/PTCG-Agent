
def register_handler_type(handler_cls):
  """Registers a checkpoint handler type in the global registry.

  The registry is keyed by the handler's typestr. If the handler does not
  provide a typestr, the default typestr is resolved from the handler's
  module and class name.

  Args:
    handler_cls: The checkpoint handler class to register.

  Returns:
    The registered checkpoint handler class.
  """
  _GLOBAL_HANDLER_TYPE_REGISTRY.add(handler_cls)
  return handler_cls

