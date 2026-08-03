import random

def stochastic_convert(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], random: _ods_ir.Value[_ods_ir.VectorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return StochasticConvertOp(output=output, input=input, random=random, loc=loc, ip=ip).result


def stochastic_convert(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], random: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return StochasticConvertOp(result=result, operand=operand, random=random, loc=loc, ip=ip).result

