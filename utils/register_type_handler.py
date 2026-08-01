
def register_type_handler(ty, handler, func):
  """Registers new func for type, and restores original handler when done."""
  original_handler = type_handler_registry.get_type_handler(ty)
  type_handler_registry.register_type_handler(
      ty, handler, func=func, override=True
  )
  try:
    yield
  finally:
    type_handler_registry.register_type_handler(
        ty, original_handler, func=func, override=True
    )


def register_type_handler(
    ty: Any,
    handler: types.TypeHandler,
    func: Optional[Callable[[Any], bool]] = None,
    override: bool = False,
):
  """Registers a type for serialization/deserialization with a given handler.

  Note that it is possible for a type to match multiple different entries in
  the registry, each with a different handler. In this case, only the first
  match is used.

  Args:
    ty: A type to register.
    handler: a TypeHandler capable of reading and writing parameters of type
      `ty`.
    func: A function that accepts a type and returns True if the type should be
      handled by the provided TypeHandler. If this parameter is not specified,
      defaults to `lambda t: issubclass(t, ty)`.
    override: if True, will override an existing mapping of type to handler.

  Raises:
    ValueError if a type is already registered and override is False.
  """
  GLOBAL_TYPE_HANDLER_REGISTRY.add(ty, handler, func, override)

