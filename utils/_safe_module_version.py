
def _safe_module_version(import_path: str) -> str:
  try:
    mod = importlib.import_module(import_path)
    return getattr(mod, "__version__", "unknown")
  except ImportError:
    return "missing"

