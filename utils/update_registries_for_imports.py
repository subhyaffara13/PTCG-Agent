import sys

def update_registries_for_imports():
  """Updates registries by running setup logic for newly-imported modules."""
  for module_name, (setup_module, setup_attribute) in tuple(
      _LAZY_MODULE_SETUP_FUNCTIONS.items()
  ):
    if module_name in sys.modules:
      module = importlib.import_module(setup_module)
      setup_fn = getattr(module, setup_attribute)
      setup_fn()
      del _LAZY_MODULE_SETUP_FUNCTIONS[module_name]

