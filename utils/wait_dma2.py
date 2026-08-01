
def wait_dma2(semaphore: _ods_ir.Value[_ods_ir.MemRefType], src: _ods_ir.Value[_ods_ir.MemRefType], dst: _ods_ir.Value[_ods_ir.MemRefType], *, device_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, core_id: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, strict_ordering: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WaitDMA2Op:
  return WaitDMA2Op(semaphore=semaphore, src=src, dst=dst, device_id=device_id, core_id=core_id, strict_ordering=strict_ordering, loc=loc, ip=ip)

