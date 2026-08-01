
def topk(k, seq, key=None):
    """ Find the k largest elements of a sequence

    Operates lazily in ``n*log(k)`` time

    >>> topk(2, [1, 100, 10, 1000])
    (1000, 100)

    Use a key function to change sorted order

    >>> topk(2, ['Alice', 'Bob', 'Charlie', 'Dan'], key=len)
    ('Charlie', 'Alice')

    See also:
        heapq.nlargest
    """
    if key is not None and not callable(key):
        key = getter(key)
    return tuple(heapq.nlargest(k, seq, key=key))


def topk(self: list[int], k: int, dim: int = -1) -> tuple[list[int], list[int]]:
    if len(self) == 0:
        result: list[int] = []
    else:
        if k > self[dim]:
            raise AssertionError(
                f"k ({k}) is too big for dimension {dim} of size {self[dim]}"
            )
        result = _copy(self)
        result[dim] = k
    return result, result


def topk(self, k, dim=-1, largest=True, sorted=True):
    if not config.triton.decompose_sort_ops:
        return topk_fallback(self, k, dim, largest, sorted)
    shape = self.get_size()
    ndim = len(shape)
    if ndim == 0:
        return clone(self), _full(0, self.get_device(), torch.int64, shape)
    dim = canonicalize_dim(ndim, dim)
    sorted_vals, sorted_idxs = sort_stable(
        self, stable=True, dim=dim, descending=largest
    )
    values = slice_(sorted_vals, dim, 0, k)
    indices = slice_(sorted_idxs, dim, 0, k)
    return values, indices


def topk(g: jit_utils.GraphContext, self, k, dim, largest, sorted, out=None):
    return symbolic_helper._topk_helper(
        g, self, k, dim, largest=largest, sorted=sorted, out=out
    )


def topk(g: jit_utils.GraphContext, self, k, dim, largest, sorted, out=None):
    return symbolic_helper._topk_helper(
        g, self, k, dim, largest=largest, sorted=sorted, out=out
    )


def topk(g: jit_utils.GraphContext, self, k, dim, largest, sorted, out=None):
    if out is not None:
        symbolic_helper._unimplemented(
            "TopK", "Out parameter is not supported for topk", self
        )
    if not largest:
        symbolic_helper._unimplemented("TopK", "Ascending TopK is not supported", self)

    return g.op("TopK", self, k_i=k, axis_i=dim, outputs=2)


def topk(operand: _ods_ir.Value[_ods_ir.RankedTensorType], k: _Union[int, _ods_ir.IntegerAttr], *, largest: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return TopKOp(operand=operand, k=k, largest=largest, results=results, loc=loc, ip=ip).results

