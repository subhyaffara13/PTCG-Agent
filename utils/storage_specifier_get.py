
def storage_specifier_get(specifier: _ods_ir.Value, specifier_kind: _Union[_Any, _ods_ir.Attribute], *, level: _Optional[_Union[_Any, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return GetStorageSpecifierOp(specifier=specifier, specifierKind=specifier_kind, level=level, results=results, loc=loc, ip=ip).result

