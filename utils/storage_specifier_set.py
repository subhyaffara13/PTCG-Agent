
def storage_specifier_set(specifier: _ods_ir.Value, specifier_kind: _Union[_Any, _ods_ir.Attribute], value: _ods_ir.Value[_ods_ir.IndexType], *, level: _Optional[_Union[_Any, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SetStorageSpecifierOp(specifier=specifier, specifierKind=specifier_kind, value=value, level=level, results=results, loc=loc, ip=ip).result

