
def shuffle(x):
    # no @normalizer because we do not cast e.g. lists to tensors
    from ._ndarray import ndarray

    if isinstance(x, torch.Tensor):
        tensor = x
    elif isinstance(x, ndarray):
        tensor = x.tensor
    else:
        raise NotImplementedError("We do not random.shuffle lists in-place")

    perm = torch.randperm(tensor.shape[0])
    xp = tensor[perm]
    tensor.copy_(xp)


def shuffle(value: _ods_ir.Value, offset: _ods_ir.Value[_ods_ir.IntegerType], width: _ods_ir.Value[_ods_ir.IntegerType], mode: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return ShuffleOp(value=value, offset=offset, width=width, mode=mode, results=results, loc=loc, ip=ip).results


def shuffle(v1: _ods_ir.Value[_ods_ir.VectorType], v2: _ods_ir.Value[_ods_ir.VectorType], mask: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ShuffleOp(v1=v1, v2=v2, mask=mask, results=results, loc=loc, ip=ip).result

