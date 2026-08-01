
def get_approximate_basis(
    A: Tensor,
    q: int,
    niter: int | None = 2,
    M: Tensor | None = None,
) -> Tensor:
    """Return tensor :math:`Q` with :math:`q` orthonormal columns such
    that :math:`Q Q^H A` approximates :math:`A`. If :math:`M` is
    specified, then :math:`Q` is such that :math:`Q Q^H (A - M)`
    approximates :math:`A - M`. without instantiating any tensors
    of the size of :math:`A` or :math:`M`.

    .. note:: The implementation is based on the Algorithm 4.4 from
              Halko et al., 2009.

    .. note:: For an adequate approximation of a k-rank matrix
              :math:`A`, where k is not known in advance but could be
              estimated, the number of :math:`Q` columns, q, can be
              chosen according to the following criteria: in general,
              :math:`k <= q <= min(2*k, m, n)`. For large low-rank
              matrices, take :math:`q = k + 5..10`.  If k is
              relatively small compared to :math:`min(m, n)`, choosing
              :math:`q = k + 0..2` may be sufficient.

    .. note:: To obtain repeatable results, reset the seed for the
              pseudorandom number generator

    Args::
        A (Tensor): the input tensor of size :math:`(*, m, n)`

        q (int): the dimension of subspace spanned by :math:`Q`
                 columns.

        niter (int, optional): the number of subspace iterations to
                               conduct; ``niter`` must be a
                               nonnegative integer. In most cases, the
                               default value 2 is more than enough.

        M (Tensor, optional): the input tensor's mean of size
                              :math:`(*, m, n)`.

    References::
        - Nathan Halko, Per-Gunnar Martinsson, and Joel Tropp, Finding
          structure with randomness: probabilistic algorithms for
          constructing approximate matrix decompositions,
          arXiv:0909.4061 [math.NA; math.PR], 2009 (available at
          `arXiv <http://arxiv.org/abs/0909.4061>`_).
    """

    niter = 2 if niter is None else niter
    dtype = _utils.get_floating_dtype(A) if not A.is_complex() else A.dtype
    matmul = _utils.matmul

    R = torch.randn(A.shape[-1], q, dtype=dtype, device=A.device)

    # The following code could be made faster using torch.geqrf + torch.ormqr
    # but geqrf is not differentiable

    X = matmul(A, R)
    if M is not None:
        X = X - matmul(M, R)
    Q = torch.linalg.qr(X).Q
    for _ in range(niter):
        X = matmul(A.mH, Q)
        if M is not None:
            X = X - matmul(M.mH, Q)
        Q = torch.linalg.qr(X).Q
        X = matmul(A, Q)
        if M is not None:
            X = X - matmul(M, Q)
        Q = torch.linalg.qr(X).Q
    return Q

