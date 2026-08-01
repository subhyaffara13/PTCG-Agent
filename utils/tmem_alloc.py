
def tmem_alloc(result: _ods_ir.Type, smem_ptr: _ods_ir.Value[_ods_ir.MemRefType], *, collective: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, packing: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return TmemAllocOp(result=result, smem_ptr=smem_ptr, collective=collective, packing=packing, loc=loc, ip=ip).result


def tmem_alloc(tmem_addr: ir.Value, ncols: int, collective: bool = False, exact: bool = True) -> tuple[ir.Value, int]:
  if isinstance(tmem_addr.type, ir.MemRefType):
    ref_ty = ir.MemRefType(tmem_addr.type)
    if ref_ty.element_type != ir.IntegerType.get_signless(32):
      raise ValueError(f"tmem_addr must be an i32 memref, got: {ref_ty}")
    if not utils.is_smem_ref(ref_ty):
      raise ValueError(f"tmem_addr must be in shared memory, got: {ref_ty}")
    if math.prod(ref_ty.shape) != 1:
      raise ValueError(f"tmem_addr must contain a single element, got: {ref_ty}")
    tmem_addr = utils.memref_ptr(tmem_addr)
  elif tmem_addr.type != llvm.PointerType.get(address_space=3):
    raise ValueError(f"tmem_addr must be an SMEM pointer or a memref, got: {tmem_addr.type}")
  ncols = tmem_alloc_exact_ncols(ncols, exact)
  group = nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1
  i32 = ir.IntegerType.get_signless(32)
  return nvvm.tcgen05_alloc(tmem_addr, utils.c(ncols, i32), group=group), ncols  # pyrefly: ignore[bad-return]

