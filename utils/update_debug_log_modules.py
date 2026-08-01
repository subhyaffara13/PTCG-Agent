
def update_debug_log_modules(module_names_str: str | None):
  _disable_all_debug_logging()
  if not module_names_str:
    return
  module_names = module_names_str.split(',')
  for module_name in module_names:
    _enable_debug_logging(module_name)

