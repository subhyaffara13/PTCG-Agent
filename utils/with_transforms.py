
def with_transforms(ref: _ods_ir.Value[_ods_ir.MemRefType], transforms: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return WithTransformsOp(ref=ref, transforms=transforms, results=results, loc=loc, ip=ip).result

