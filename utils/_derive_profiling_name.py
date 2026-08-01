
def _derive_profiling_name(module, fn):
  fn_name = _get_fn_name(fn)
  method_suffix = f'.{fn_name}' if fn_name != '__call__' else ''
  module_name = module.name or module.__class__.__name__
  return f'{module_name}{method_suffix}'

