
def _CanImport(mod_name):
  try:
    mod = importlib.import_module(mod_name)
    # Work around a known issue in the classic bootstrap .par import hook.
    if not mod:
      raise ImportError(mod_name + ' import succeeded but was None')
    return True
  except ImportError:
    return False

