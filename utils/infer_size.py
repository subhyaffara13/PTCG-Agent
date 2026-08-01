
def infer_size(shape: ShapeType, numel: int) -> tuple[int, ...]:
    """
    Infers the size of a dim with size -1, if it exists.
    Also checks that new shape is compatible with the number of elements.
    """
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    dim = None
    newsize = 1
    for i, d in enumerate(shape):
        if guard_or_false(d == -1):
            torch._check(dim is None, lambda: "only one dimension can be inferred")
            dim = i
        else:
            torch._check(
                d >= 0,
                lambda: (
                    f"invalid shape dimension {d}. If this was symbolic, it was assumed to not be -1."
                    "If this was meant to be inferred, please explicitly pass in -1."
                ),
            )
            newsize *= d
    if dim is None:
        torch._check(
            numel == newsize,
            lambda: f"shape '{list(shape)}' is invalid for input of size {numel}",
        )
    else:
        torch._check(
            newsize != 0,
            lambda: (
                f"cannot reshape tensor of 0 elements into shape {list(shape)} because the "
                f"unspecified dimension size -1 can be any value and is ambiguous"
                if guard_or_false(numel == 0)
                else f"shape '{list(shape)}' is invalid for input of size {numel}"
            ),
        )
        torch._check(
            numel % newsize == 0,
            lambda: f"shape '{list(shape)}' is invalid for input of size {numel}",
        )
        # Convert to list to produce a compatible error message with core
        # PyTorch, which prints sequences in square brackets.
        shape = list(shape)
        shape[dim] = numel // newsize
        torch._check(shape[dim] >= 0)
    return tuple(shape)


def infer_size(
    a: Sequence[IntLikeType], b: Sequence[IntLikeType]
) -> tuple[IntLikeType, ...]:
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    dimsA = len(a)
    dimsB = len(b)
    ndim = max(dimsA, dimsB)
    expandedSizes: list[IntLikeType] = [0] * ndim
    for i in range(ndim - 1, -1, -1):
        offset = ndim - 1 - i
        dimA = dimsA - 1 - offset
        dimB = dimsB - 1 - offset
        sizeA = a[dimA] if dimA >= 0 else 1
        sizeB = b[dimB] if dimB >= 0 else 1

        # NB: It is very important to test for broadcasting, before testing
        # sizeA == sizeB.  This is because the broadcasting tests are likely
        # to be statically known (in particular, if sizeA/sizeB is unbacked
        # but size-like, we will unsoundly assume they never equal 1), but
        # the sizeA == sizeB test may not be statically known.  However, once
        # we have established that no broadcasting is happening, the
        # sizeA == sizeB is now expect_true and we can defer it as a runtime
        # assert (this works because Python will return the terminal
        # expression of an or statement as-is, without bool()'ing it; if this
        # were not the case, we'd need to write this using torch.sym_or() or
        # something like that).
        torch._check(
            guard_or_false(sizeA == 1) or guard_or_false(sizeB == 1) or sizeA == sizeB,
            lambda: f"The size of tensor a ({sizeA}) "
            f"must match the size of tensor b ({sizeB}) "
            f"at non-singleton dimension {i})",
        )
        expandedSizes[i] = sizeB if guard_or_false(sizeA == 1) else sizeA
    return tuple(expandedSizes)


def infer_size(total_size: int, sizes: Shape) -> Shape:
    """
    One dimension input to view may be "-1".

    Infer the size of this dimension given the total_size.
    """
    from torch.fx.experimental.symbolic_shapes import guard_or_false

    infers = [i for i, s in enumerate(sizes) if guard_or_false(s == -1)]
    size = prod(sizes)
    if not len(infers) <= 1:
        raise AssertionError("can only infer one size")
    if infers:
        size = -size
        missing_size = total_size // size
        torch._check(
            total_size % size == 0,
            lambda: f"size inferred for -1 is not integral {sizes} should have {total_size} elements.",
        )
        return tuple(s if not guard_or_false(s == -1) else missing_size for s in sizes)
    torch._check(
        size == total_size,
        lambda: f"sizes do not match {total_size} vs {size}",
    )
    return sizes

