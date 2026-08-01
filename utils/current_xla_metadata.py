
def current_xla_metadata() -> dict[str, Any] | None:
  metadata = config.xla_metadata_context_manager.value
  return None if metadata is None else metadata.val

