
def intr_expect_with_probability(val: _ods_ir.Value[_ods_ir.IntegerType], expected: _ods_ir.Value[_ods_ir.IntegerType], prob: _Union[float, _ods_ir.FloatAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExpectWithProbabilityOp(val=val, expected=expected, prob=prob, results=results, loc=loc, ip=ip).result

