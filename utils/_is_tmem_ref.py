
def _is_tmem_ref(v: ir.Value) -> bool:
  return isinstance(v.type, ir.MemRefType) and utils.is_tmem_ref(v)

