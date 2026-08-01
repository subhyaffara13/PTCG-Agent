
def _has_communication(module, **_):
  if launch_context.uses_collective_metadata(module):
    return True
  empty_str_attr = ir.StringAttr.get("")
  for op in module.body:
    if "nvshmem" in getattr(op, "sym_name", empty_str_attr).value:
      return True
  return False

