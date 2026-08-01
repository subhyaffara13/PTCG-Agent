
def index_select(self: list[int], dim: int, index: list[int]):
    dim = maybe_wrap_dim(dim, len(self))
    numel = multiply_integers(index)
    if len(index) > 1:
        raise AssertionError(f"Expected len(index) <= 1, but got {len(index)}")
    if not (dim == 0 or dim < len(self)):
        raise AssertionError(
            f"Expected dim ({dim}) == 0 or dim < len(self) ({len(self)})"
        )
    result_size: list[int] = []
    for i in range(len(self)):
        if dim == i:
            result_size.append(numel)
        else:
            result_size.append(self[i])
    return result_size


def index_select(x: TensorLike, dim: int, index: TensorLike):
    dim = utils.canonicalize_dims(x.ndim, dim)
    torch._check(
        index.ndim <= 1,
        lambda: f"Index should have dimension 1 or 0 (got {index.ndim})",
    )
    if index.ndim == 0:
        index = index.unsqueeze(0)
    if x.ndim == 0:
        # Treat scalars as elements of \R^1
        # We cannot use x[idx] here as it accesses item() (??), hence this awkward construction
        return torch.empty_like(x).index_copy(0, index, x.expand_as(index))

    idx = (slice(None),) * dim + (index,)
    return x[idx].contiguous(memory_format=utils.suggest_memory_format(x))


def index_select(g: jit_utils.GraphContext, self, dim, index):
    # In case of a scalar index, index_select returns a tensor with the same rank as the input.
    # To match this behavior in ONNX, we make index a 1D tensor so that the following gather
    # also produces a tensor with the same rank as the input.
    return symbolic_helper._select_helper(g, self, dim, index)

