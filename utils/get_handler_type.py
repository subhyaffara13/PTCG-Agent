
def get_handler_type(handler_typestr: str) -> Type[CheckpointHandler]:
  return _GLOBAL_HANDLER_TYPE_REGISTRY.get(handler_typestr)

