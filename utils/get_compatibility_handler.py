
def get_compatibility_handler(
    handler: handler_types.CheckpointableHandler,
) -> CompatibilityCheckpointHandler:

  class _CompatibilityHandler(CompatibilityCheckpointHandler):

    @classmethod
    def typestr(cls) -> str:
      return handler_types.typestr(type(handler))

  return _CompatibilityHandler(handler)

