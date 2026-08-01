
def linalg_lu_factor_ex_meta(
    A: Tensor,
    *,
    pivot: bool = True,
    check_errors: bool = False,
) -> tuple[Tensor, Tensor, Tensor]:
    torch._check(
        A.ndim >= 2,
        lambda: f"torch.lu_factor: Expected tensor with 2 or more dimensions. Got size: {A.shape} instead",
    )

    sizes = list(A.shape)
    m = sizes[-2]
    n = sizes[-1]

    LU = torch.empty_strided(
        size=sizes,
        stride=make_contiguous_strides_for(sizes, row_major=False),
        dtype=A.dtype,
        device=A.device,
    )

    # Sets sizes to the size of pivots
    sizes.pop()
    # Use sym_min to handle unbacked symbolic dimensions
    sizes[-1] = sym_min(m, n)
    pivots = A.new_empty(sizes, dtype=torch.int)

    # Sets sizes to the size of info
    sizes.pop()
    info = A.new_empty(sizes, dtype=torch.int)

    return LU, pivots, info

