
def named_metadata(metadata_name: _Union[str, _ods_ir.StringAttr], nodes: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> NamedMetadataOp:
  return NamedMetadataOp(metadata_name=metadata_name, nodes=nodes, loc=loc, ip=ip)

