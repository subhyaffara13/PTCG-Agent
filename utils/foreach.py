
def foreach(triton_meta, filename=None, inductor_meta=None):
    """
    Compile a triton foreach kernel
    """
    configs = []

    # Naive autotuning path for num_warps
    if not (
        inductor_meta.get("max_autotune") or inductor_meta.get("max_autotune_pointwise")
    ):
        configs.append(triton.Config({}, num_stages=1, num_warps=8))
    else:
        for warps in [1, 2, 4, 8]:
            configs.append(triton.Config({}, num_stages=1, num_warps=warps))

    return cached_autotune(
        None,
        configs,
        triton_meta=triton_meta,
        inductor_meta=inductor_meta,
        heuristic_type=HeuristicType.TEMPLATE,
        filename=filename,
    )


def foreach(results_: _Sequence[_ods_ir.Type], tensor: _ods_ir.Value[_ods_ir.RankedTensorType], init_args: _Sequence[_ods_ir.Value], *, order: _Optional[_Union[_ods_ir.AffineMap, _ods_ir.AffineMapAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ForeachOp]:
  op = ForeachOp(results_=results_, tensor=tensor, initArgs=init_args, order=order, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

