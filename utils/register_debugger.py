
def register_debugger(name: str, debugger: Debugger, priority: int) -> None:
  if name in _debugger_registry:
    raise ValueError(f"Debugger with name \"{name}\" already registered.")
  _debugger_registry[name] = (priority, debugger)

