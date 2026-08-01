
def register_compilation_handler(
    platform: str, handler: CompilationHandler
) -> None:
  platform = platform.upper()
  with _compilation_handlers_lock:
    if existing_handler := _compilation_handlers.get(platform):
      raise RuntimeError(
          f'Platform {platform} already has a Triton compilation handler:'
          f' {existing_handler}'
      )
    _compilation_handlers[platform] = handler

