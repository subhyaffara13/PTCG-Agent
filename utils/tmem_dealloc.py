
def tmem_dealloc(tmem_ref: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmemDeallocOp:
  return TmemDeallocOp(tmem_ref=tmem_ref, loc=loc, ip=ip)


def tmem_dealloc(tmem_addr: ir.Value, ncols: int, collective: bool = False, exact: bool = True) -> None:
  if tmem_addr.type != ir.IntegerType.get_signless(32):
    raise ValueError(f"tmem_addr must be an i32, got: {tmem_addr.type}")
  ncols = tmem_alloc_exact_ncols(ncols, exact)
  group = nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1
  i32 = ir.IntegerType.get_signless(32)
  nvvm.tcgen05_dealloc(
      _tmem_addr_to_ptr(tmem_addr), utils.c(ncols, i32), group=group
  )

