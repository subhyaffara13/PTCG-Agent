from typing import Optional

def for_(
    start,
    stop=None,
    step=None,
    iter_args: Optional[Sequence[Value]] = None,
    *,
    loc=None,
    ip=None,
):
    if step is None:
        step = 1
    if stop is None:
        stop = start
        start = 0
    params = [start, stop, step]
    for i, p in enumerate(params):
        if isinstance(p, int):
            p = constant(IndexType.get(), p)
        elif isinstance(p, float):
            raise ValueError(f"{p=} must be int.")
        params[i] = p

    start, stop, step = params

    for_op = ForOp(start, stop, step, iter_args, loc=loc, ip=ip)
    iv = for_op.induction_variable
    iter_args = tuple(for_op.inner_iter_args)
    with InsertionPoint(for_op.body):
        if len(iter_args) > 1:
            yield iv, iter_args, for_op.results
        elif len(iter_args) == 1:
            yield iv, iter_args[0], for_op.results[0]
        else:
            yield iv


def for_(results_: _Sequence[_ods_ir.Type], tensors: _Sequence[_ods_ir.Value], iterations: _Union[int, _ods_ir.IntegerAttr], *, unroll_factor: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ForOp]:
  op = ForOp(results_=results_, tensors=tensors, iterations=iterations, unroll_factor=unroll_factor, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def for_(results_: _Sequence[_ods_ir.Type], lower_bound: _ods_ir.Value, upper_bound: _ods_ir.Value, step: _ods_ir.Value, init_args: _Sequence[_ods_ir.Value], *, unsigned_cmp: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ForOp]:
  op = ForOp(results_=results_, lowerBound=lower_bound, upperBound=upper_bound, step=step, initArgs=init_args, unsignedCmp=unsigned_cmp, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

