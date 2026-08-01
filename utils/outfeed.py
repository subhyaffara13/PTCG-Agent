
def outfeed(inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], token: _ods_ir.Value, *, outfeed_config: _Optional[_Union[str, _ods_ir.StringAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return OutfeedOp(inputs=inputs, token=token, outfeed_config=outfeed_config, results=results, loc=loc, ip=ip).result


def outfeed(inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], token: _ods_ir.Value, *, outfeed_config: _Optional[_Union[str, _ods_ir.StringAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return OutfeedOp(inputs=inputs, token=token, outfeed_config=outfeed_config, results=results, loc=loc, ip=ip).result

