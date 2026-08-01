
def diagonal_scatter(input, src, offset: int = 0, dim1: int = 0, dim2: int = 1):
    output = clone(input)
    target = diagonal(output, offset, dim1, dim2)
    mutate_to(target, src)
    return output


def diagonal_scatter(
    input: TensorLikeType,
    src: TensorLikeType,
    offset: int = 0,
    dim1: int = 0,
    dim2: int = 1,
) -> TensorLikeType:
    from torch.fx.experimental.symbolic_shapes import guard_or_false, sym_or

    out = utils.clone_preserve_strides(input)
    diag = out.diagonal(offset, dim1, dim2)
    # Use sym_or + guard_or_false to handle unbacked symbolic dimensions.
    torch._check(
        diag.ndim == src.ndim
        and not guard_or_false(
            sym_or(*(d1 != d2 for d1, d2 in zip(diag.shape, src.shape)))
        ),
        lambda: "expected src to have a size equal to the diagonal of the input."
        f"Got {src.shape} for a diagonal of shape {diag.shape}",
    )
    copy_to(diag, src)
    return out

