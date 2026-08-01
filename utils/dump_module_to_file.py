
def dump_module_to_file(module: ir.Module, stage_name: str) -> str | None:
  """Dumps the `module` IR to a file.

  Dumps the module if JAX_DUMP_IR_TO is defined.

  Args:
    module: The module to dump
    stage_name: A name to distinguish different stages of a module, will be
      appended to the `module.name`.

  Returns:
    The name of the file containing the dump if JAX_DUMP_IR_TO is defined and
    the module was dumped, `None` otherwise.
  """
  if not (out_dir := path.make_jax_dump_dir(config.jax_dump_ir_to.value)):
    return None
  modes = config.jax_dump_ir_modes.value.split(',')
  if 'stablehlo' not in modes:
    return None
  id = next(_ir_dump_counter)
  sym_name = module.operation.attributes['sym_name']
  module_name = ir.StringAttr(sym_name).value

  name = f"jax_ir{id:04d}_{_make_string_safe_for_filename(module_name)}_{stage_name}.mlir"

  full_path = out_dir / name
  full_path.write_text(module_to_string(module))
  return name

