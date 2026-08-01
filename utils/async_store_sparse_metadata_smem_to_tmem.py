
def async_store_sparse_metadata_smem_to_tmem(source: _ods_ir.Value[_ods_ir.MemRefType], destination: _ods_ir.Value[_ods_ir.MemRefType], *, collective: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> AsyncStoreSparseMetadataSmemToTmemOp:
  return AsyncStoreSparseMetadataSmemToTmemOp(source=source, destination=destination, collective=collective, loc=loc, ip=ip)

