
def linalg_lu_meta(A: Tensor, *, pivot: bool = True) -> tuple[Tensor, Tensor, Tensor]:
    torch._check(
        A.ndim >= 2,
        lambda: f"linalg.lu: Expected tensor with 2 or more dimensions. Got size: {A.shape} instead",
    )

    sizes = list(A.shape)
    m = sizes[-2]
    n = sizes[-1]
    # Use sym_min to handle unbacked symbolic dimensions
    k = sym_min(m, n)

    sizes[-1] = m
    if pivot:
        P = A.new_empty(sizes)
    else:
        P = A.new_empty([0])

    sizes[-1] = k
    L = A.new_empty(sizes)

    sizes[-2] = k
    sizes[-1] = n
    U = A.new_empty(sizes)
    return P, L, U

