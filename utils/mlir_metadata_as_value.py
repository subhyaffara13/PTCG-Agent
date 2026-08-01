
def mlir_metadata_as_value(metadata: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MetadataAsValueOp(metadata=metadata, results=results, loc=loc, ip=ip).result

