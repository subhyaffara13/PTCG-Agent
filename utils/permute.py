
def permute(input: list[int], dims: list[int]):
    if len(input) != len(dims):
        raise AssertionError(
            f"Expected len(input) ({len(input)}) == len(dims) ({len(dims)})"
        )
    ndim = len(dims)
    seen_dims: list[int] = []
    newSizes: list[int] = []
    for i in range(ndim):
        dim = maybe_wrap_dim(dims[i], ndim)
        seen_dims.append(dim)
        newSizes.append(input[dim])
    for i in range(1, ndim):
        for j in range(i):
            if seen_dims[i] == seen_dims[j]:
                raise AssertionError(
                    f"Repeated dimension {seen_dims[i]} in permute dimensions"
                )
    return newSizes


def permute(x, dims):
    assert isinstance(x, TensorBox)
    assert isinstance(dims, (list, tuple))
    return TensorBox(PermuteView.create(x.data, tuple(dims)))


def permute(a: TensorLikeType, *dims) -> TensorLikeType:
    _permutation = utils.canonicalize_dims(
        a.ndim, utils.extract_dims_from_varargs(dims)
    )
    return prims.transpose(a, _permutation)


def permute(g: jit_utils.GraphContext, self, dims):
    if dims == list(range(len(dims))):
        return self
    return g.op("Transpose", self, perm_i=dims)

