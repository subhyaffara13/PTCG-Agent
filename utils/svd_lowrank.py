
def svd_lowrank(
    A: Tensor,
    q: int | None = 6,
    niter: int | None = 2,
    M: Tensor | None = None,
) -> tuple[Tensor, Tensor, Tensor]:
    r"""Return the singular value decomposition ``(U, S, V)`` of a matrix,
    batches of matrices, or a sparse matrix :math:`A` such that
    :math:`A \approx U \operatorname{diag}(S) V^{\text{H}}`. In case :math:`M` is given, then
    SVD is computed for the matrix :math:`A - M`.

    .. note:: The implementation is based on the Algorithm 5.1 from
              Halko et al., 2009.

    .. note:: For an adequate approximation of a k-rank matrix
              :math:`A`, where k is not known in advance but could be
              estimated, the number of :math:`Q` columns, q, can be
              chosen according to the following criteria: in general,
              :math:`k <= q <= min(2*k, m, n)`. For large low-rank
              matrices, take :math:`q = k + 5..10`.  If k is
              relatively small compared to :math:`min(m, n)`, choosing
              :math:`q = k + 0..2` may be sufficient.

    .. note:: This is a randomized method. To obtain repeatable results,
              set the seed for the pseudorandom number generator

    .. note:: In general, use the full-rank SVD implementation
              :func:`torch.linalg.svd` for dense matrices due to its 10x
              higher performance characteristics. The low-rank SVD
              will be useful for huge sparse matrices that
              :func:`torch.linalg.svd` cannot handle.

    Args::
        A (Tensor): the input tensor of size :math:`(*, m, n)`

        q (int, optional): a slightly overestimated rank of A.

        niter (int, optional): the number of subspace iterations to
                               conduct; niter must be a nonnegative
                               integer, and defaults to 2

        M (Tensor, optional): the input tensor's mean of size
                              :math:`(*, m, n)`, which will be broadcasted
                              to the size of A in this function.

    References::
        - Nathan Halko, Per-Gunnar Martinsson, and Joel Tropp, Finding
          structure with randomness: probabilistic algorithms for
          constructing approximate matrix decompositions,
          arXiv:0909.4061 [math.NA; math.PR], 2009 (available at
          `arXiv <https://arxiv.org/abs/0909.4061>`_).

    """
    if not torch.jit.is_scripting():
        tensor_ops = (A, M)
        if not set(map(type, tensor_ops)).issubset(
            (torch.Tensor, type(None))
        ) and has_torch_function(tensor_ops):
            return handle_torch_function(
                svd_lowrank, tensor_ops, A, q=q, niter=niter, M=M
            )
    return _svd_lowrank(A, q=q, niter=niter, M=M)

