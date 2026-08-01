
def _svd_lowrank(
    A: Tensor,
    q: int | None = 6,
    niter: int | None = 2,
    M: Tensor | None = None,
) -> tuple[Tensor, Tensor, Tensor]:
    # Algorithm 5.1 in Halko et al., 2009

    q = 6 if q is None else q
    m, n = A.shape[-2:]
    matmul = _utils.matmul
    if M is not None:
        M = M.broadcast_to(A.size())

    # Assume that A is tall
    if m < n:
        A = A.mH
        if M is not None:
            M = M.mH

    Q = get_approximate_basis(A, q, niter=niter, M=M)
    B = matmul(Q.mH, A)
    if M is not None:
        B = B - matmul(Q.mH, M)
    U, S, Vh = torch.linalg.svd(B, full_matrices=False)
    V = Vh.mH
    U = Q.matmul(U)

    if m < n:
        U, V = V, U

    return U, S, V

