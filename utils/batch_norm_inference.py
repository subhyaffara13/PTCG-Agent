
def batch_norm_inference(operand: _ods_ir.Value[_ods_ir.RankedTensorType], scale: _ods_ir.Value[_ods_ir.RankedTensorType], offset: _ods_ir.Value[_ods_ir.RankedTensorType], mean: _ods_ir.Value[_ods_ir.RankedTensorType], variance: _ods_ir.Value[_ods_ir.RankedTensorType], epsilon: _Union[float, _ods_ir.FloatAttr], feature_index: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BatchNormInferenceOp(operand=operand, scale=scale, offset=offset, mean=mean, variance=variance, epsilon=epsilon, feature_index=feature_index, results=results, loc=loc, ip=ip).result


def batch_norm_inference(operand: _ods_ir.Value[_ods_ir.RankedTensorType], scale: _ods_ir.Value[_ods_ir.RankedTensorType], offset: _ods_ir.Value[_ods_ir.RankedTensorType], mean: _ods_ir.Value[_ods_ir.RankedTensorType], variance: _ods_ir.Value[_ods_ir.RankedTensorType], epsilon: _Union[float, _ods_ir.FloatAttr], feature_index: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BatchNormInferenceOp(operand=operand, scale=scale, offset=offset, mean=mean, variance=variance, epsilon=epsilon, feature_index=feature_index, results=results, loc=loc, ip=ip).result

