
def dump_module_message(module: ir.Module, stage_name: str) -> str:
  dumped_to = dump_module_to_file(module, stage_name)
  if dumped_to:
    return f"The module was dumped to {dumped_to}."
  else:
    return "Define JAX_DUMP_IR_TO to dump the module."

