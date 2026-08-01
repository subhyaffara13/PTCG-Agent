
def movedim(self: list[int], source: list[int], destination: list[int]) -> list[int]:
    self_dim = len(self)
    if self_dim <= 1:
        return self
    normalized_src: list[int] = []
    normalized_dst: list[int] = []
    for i in range(len(source)):
        normalized_src.append(maybe_wrap_dim(source[i], self_dim))
        normalized_dst.append(maybe_wrap_dim(destination[i], self_dim))
    order = [-1 for i in range(self_dim)]
    src_dims = [i for i in range(self_dim)]
    dst_dims = [i for i in range(self_dim)]

    for i in range(len(source)):
        order[normalized_dst[i]] = normalized_src[i]
        src_dims[normalized_src[i]] = -1
        dst_dims[normalized_dst[i]] = -1

    source_dims: list[int] = []
    destination_dims: list[int] = []
    for ele in src_dims:
        if ele != -1:
            source_dims.append(ele)
    for ele in dst_dims:
        if ele != -1:
            destination_dims.append(ele)

    rest_dim = self_dim - len(source)
    for i in range(rest_dim):
        order[destination_dims[i]] = source_dims[i]
    return permute(self, order)


def movedim(
    input: TensorLikeType,
    source: int | DimsSequenceType,
    destination: int | DimsSequenceType,
) -> TensorLikeType:
    """
    Reference implementation of torch.movedim
    """
    if type(source) is int:
        source = (source,)
    if type(destination) is int:
        destination = (destination,)

    # Converts to list to produce a compatible error message with core PyTorch,
    # which prints sequences in square brackets.
    torch._check(
        len(source) == len(destination),  # type: ignore[arg-type]
        lambda: (
            "movedim: Invalid source or destination dims: source "  # type: ignore[arg-type]
            f"({list(source)} dims) should contain the same number "  # type: ignore[arg-type]
            f"of dims as destination ({list(destination)} dims)"  # type: ignore[arg-type]
        ),
    )

    rank = input.ndim
    ss = tuple(utils.canonicalize_dims(rank=rank, indices=source))  # type: ignore[arg-type]
    ds = tuple(utils.canonicalize_dims(rank=rank, indices=destination))  # type: ignore[arg-type]

    sss = set(ss)
    dss = set(ds)

    # See above on why this converts to list in error messages.
    torch._check(
        len(ss) == len(sss),
        lambda: f"movedim: repeated dim in `source` ({list(source)})",  # type: ignore[arg-type]
    )
    torch._check(
        len(ds) == len(dss),
        lambda: f"movedim: repeated dim in `destination` ({list(destination)})",  # type: ignore[arg-type]
    )

    m = dict(zip(ds, ss))
    dims = []
    si = 0  # source index
    for di in range(rank):
        # check if the destination index is in the mapping
        s = m.get(di)
        if s is not None:
            # insert source index if found
            dims.append(s)
        else:
            # insert source index sequentially, skipping indices from the mapping
            while si in sss:
                si += 1
            dims.append(si)
            si += 1

    result = torch.permute(input, tuple(dims))

    return result


def movedim(g: jit_utils.GraphContext, self, source, destination):
    # This is a pythonic implementation mostly taken from aten/src/ATen/native/TensorShape.cpp::movedim
    source = source.view(-1)
    destination = destination.view(-1)

    if source.size() != destination.size():
        raise AssertionError(
            f"source.size()={source.size()} != destination.size()={destination.size()}"
        )

    if (source == destination).all():
        return self

    self_rank = symbolic_helper._get_tensor_rank(self)
    if self_rank is None:
        raise AssertionError("self_rank must be non-None")

    perm = list(range(self_rank))

    src_dims = perm.copy()
    dst_dims = perm.copy()

    for src, dst in zip(source.tolist(), destination.tolist()):
        perm[dst] = src
        src_dims[src] = -1
        dst_dims[dst] = -1

    src_dims = [dim for dim in src_dims if dim != -1]
    dst_dims = [dim for dim in dst_dims if dim != -1]

    for src, dst in zip(src_dims, dst_dims):
        perm[dst] = src

    return g.op("Transpose", self, perm_i=perm)

