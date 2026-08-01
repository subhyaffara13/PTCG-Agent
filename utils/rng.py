
def rng():
    rng = np.random.default_rng(1718313768084012)
    yield rng


def rng(a: _ods_ir.Value[_ods_ir.RankedTensorType], b: _ods_ir.Value[_ods_ir.RankedTensorType], shape: _ods_ir.Value[_ods_ir.RankedTensorType], rng_distribution: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RngOp(a=a, b=b, shape=shape, rng_distribution=rng_distribution, results=results, loc=loc, ip=ip).result


def rng(a: _ods_ir.Value[_ods_ir.RankedTensorType], b: _ods_ir.Value[_ods_ir.RankedTensorType], shape: _ods_ir.Value[_ods_ir.RankedTensorType], rng_distribution: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RngOp(a=a, b=b, shape=shape, rng_distribution=rng_distribution, results=results, loc=loc, ip=ip).result

