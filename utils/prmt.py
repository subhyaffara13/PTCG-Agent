
def prmt(lo: _ods_ir.Value[_ods_ir.IntegerType], selector: _ods_ir.Value[_ods_ir.IntegerType], mode: _Union[_Any, _ods_ir.Attribute], *, hi: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return PermuteOp(lo=lo, selector=selector, mode=mode, hi=hi, results=results, loc=loc, ip=ip).result


def prmt(high: ir.Value, low: ir.Value, permutation: ir.Value):
  i32 = ir.IntegerType.get_signless(32)
  if (result_type := high.type) != low.type:
    raise ValueError(f"Types must match, got {high.type} and {low.type}")
  if high.type != i32:
    high = bitcast(high, i32)
  if low.type != i32:
    low = bitcast(low, i32)
  if permutation.type != i32:
    permutation = bitcast(permutation, i32)
  result = llvm.inline_asm(
      i32, [high, low, permutation], "prmt.b32 $0, $1, $2, $3;", "=r,r,r,r"
  )
  assert isinstance(result, ir.Value)
  return bitcast(result, result_type)

