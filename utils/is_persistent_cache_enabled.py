
def is_persistent_cache_enabled() -> bool:
  return (config.compilation_cache_dir.value is not None
          and config.enable_compilation_cache.value)

