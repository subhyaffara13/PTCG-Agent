
def _register_submodule(module: LazyModule, name: str) -> LazyModule:
  child_module = LazyModule(
      module_name=f"{module.module_name}.{name}",
      adhoc_kwargs=module.adhoc_kwargs,
      error_callback=module.error_callback,
      success_callback=module.success_callback,
  )
  module._submodules[name] = child_module  # pylint: disable=protected-access
  return child_module

