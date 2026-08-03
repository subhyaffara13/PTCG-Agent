import sys

def _clear_parent_module_attr(module_name: str) -> None:
  """Remove parent reference (e.g. `path.to.child` -> `path.to`."""
  if '.' not in module_name:
    return
  parent_module_name, child_name = module_name.rsplit('.', 1)
  parent_module = sys.modules.get(parent_module_name)
  if not parent_module:
    return
  if hasattr(parent_module, child_name):
    delattr(parent_module, child_name)

