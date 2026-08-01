
def validate_and_process_item_handlers(
    item_handlers: Any,
) -> (
    CompositeCheckpointHandlerTypeStrs[str, Any]
    | CheckpointHandlerTypeStr
    | None
):
  """Validates and processes item_handlers field."""
  if item_handlers is None:
    return None

  _validate_type(item_handlers, [dict, str])
  if isinstance(item_handlers, CompositeCheckpointHandlerTypeStrs):
    for k in item_handlers or {}:
      _validate_type(k, str)
    return item_handlers
  elif isinstance(item_handlers, CheckpointHandlerTypeStr):
    return item_handlers

