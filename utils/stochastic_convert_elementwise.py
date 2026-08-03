import random

def stochastic_convert_elementwise(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], random: _ods_ir.Value[_ods_ir.VectorType], dst_type: _Union[_ods_ir.Type, _ods_ir.TypeAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return StochasticConvertElementwiseOp(output=output, input=input, random=random, dst_type=dst_type, loc=loc, ip=ip).result

