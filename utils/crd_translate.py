
def crd_translate(out_crds: _Sequence[_ods_ir.Type], in_crds: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], direction: _Union[_Any, _ods_ir.Attribute], encoder: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CrdTranslateOp]:
  op = CrdTranslateOp(out_crds=out_crds, in_crds=in_crds, direction=direction, encoder=encoder, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

