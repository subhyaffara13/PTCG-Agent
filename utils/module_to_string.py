
def module_to_string(module: ir.Module, enable_debug_info=None) -> str:
  output = io.StringIO()
  if enable_debug_info is None:
    enable_debug_flag = str(config.jax_include_debug_info_in_dumps.value).lower()
    enable_debug_info = enable_debug_flag not in ('false', '0')
  module.operation.print(file=output, enable_debug_info=enable_debug_info)
  return output.getvalue()

