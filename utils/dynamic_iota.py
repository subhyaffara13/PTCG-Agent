
def dynamic_iota(result: _ods_ir.Type, output_shape: _ods_ir.Value[_ods_ir.RankedTensorType], iota_dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicIotaOp(result=result, output_shape=output_shape, iota_dimension=iota_dimension, loc=loc, ip=ip).result


def dynamic_iota(result: _ods_ir.Type, output_shape: _ods_ir.Value[_ods_ir.RankedTensorType], iota_dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return DynamicIotaOp(result=result, output_shape=output_shape, iota_dimension=iota_dimension, loc=loc, ip=ip).result

