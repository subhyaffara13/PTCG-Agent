
def log_compilations():
  """A utility for programmatically capturing JAX compilation logs."""
  with _compilation_log_lock, jax.log_compiles():
    _LOG_LIST.clear()
    compilation_logs = []
    yield compilation_logs  # these will contain the compilation logs
    compilation_logs.extend([
        log for log in _LOG_LIST
        if re.search(r"Finished .* compilation", log.getMessage())
    ])

