
def _import_symbol(import_qualname: str, parent_module_name: str) -> Any:
  """Import the lazy-symbol."""
  module_name, obj_name = import_qualname.rsplit('.', 1)
  if module_name == parent_module_name:
    # To avoid infinite recursion, import sub-modules as
    # `import parent_module.submodule` rather than
    # `from parent_module import submodule`
    module = __import__(f'{module_name}.{obj_name}')
    parts = module_name.split('.')[1:] + [obj_name]
    for name in parts:
      module = getattr(module, name)
    return module
  else:
    # Import symbols as `from module import obj` to supports functions,
    # classes, etc.
    module = __import__(module_name, fromlist=[obj_name])
    return getattr(module, obj_name)

