
def enqueue_indirect_dma(source: _ods_ir.Value[_ods_ir.MemRefType], target: _ods_ir.Value[_ods_ir.MemRefType], offsets: _ods_ir.Value, semaphore: _ods_ir.Value[_ods_ir.MemRefType], *, offset_filter: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, add: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> EnqueueIndirectDMAOp:
  return EnqueueIndirectDMAOp(source=source, target=target, offsets=offsets, semaphore=semaphore, offset_filter=offset_filter, add=add, loc=loc, ip=ip)

