
def _load_source(module_name: str, module_path: str) -> types.ModuleType:
  """Loads a Python module from its source file.

  Args:
    module_name: name of the module in sys.modules.
    module_path: path to the Python file containing the module.

  Returns:
    The loaded Python module.
  """
  loader = importlib.machinery.SourceFileLoader(module_name, module_path)
  return loader.load_module()

