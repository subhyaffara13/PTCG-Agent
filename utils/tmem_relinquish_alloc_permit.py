
def tmem_relinquish_alloc_permit(*, collective: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TmemRelinquishAllocPermitOp:
  return TmemRelinquishAllocPermitOp(collective=collective, loc=loc, ip=ip)


def tmem_relinquish_alloc_permit(collective: bool) -> None:
  group = nvvm.CTAGroupKind.CTA_2 if collective else nvvm.CTAGroupKind.CTA_1
  nvvm.tcgen05_relinquish_alloc_permit(group=group)

