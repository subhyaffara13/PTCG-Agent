
def get_debugger(backend: str | None = None) -> Debugger:
  if backend is not None and backend in _debugger_registry:
    return _debugger_registry[backend][1]
  debuggers = sorted(_debugger_registry.values(), key=lambda x: -x[0])
  if not debuggers:
    raise ValueError("No debuggers registered!")
  return debuggers[0][1]

