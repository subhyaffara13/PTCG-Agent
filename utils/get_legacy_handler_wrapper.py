
def get_legacy_handler_wrapper(
    handler: checkpoint_handler.CheckpointHandler,
) -> checkpoint_handler.CheckpointHandler:
  if isinstance(handler, async_checkpoint_handler.AsyncCheckpointHandler):
    return _AsyncLegacyCheckpointHandlerWrapper(handler)
  return _LegacyCheckpointHandlerWrapper(handler)

