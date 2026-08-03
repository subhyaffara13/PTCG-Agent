from typing import Any

def _module_fingerprint(module: Module) -> tuple[type[Any], Any]:
  return _fingerprint_recursive(module, (), {})

