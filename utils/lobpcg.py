
def lobpcg(
    A: Tensor,
    k: int | None = None,
    B: Tensor | None = None,
    X: Tensor | None = None,
    n: int | None = None,
    iK: Tensor | None = None,
    niter: int | None = None,
    tol: float | None = None,
    largest: bool | None = None,
    method: str | None = None,
    tracker: None = None,
    ortho_iparams: dict[str, int] | None = None,
    ortho_fparams: dict[str, float] | None = None,
    ortho_bparams: dict[str, bool] | None = None,
) -> tuple[Tensor, Tensor]:
    """Find the k largest (or smallest) eigenvalues and the corresponding
    eigenvectors of a symmetric positive definite generalized
    eigenvalue problem using matrix-free LOBPCG methods.

    This function is a front-end to the following LOBPCG algorithms
    selectable via `method` argument:

      `method="basic"` - the LOBPCG method introduced by Andrew
      Knyazev, see [Knyazev2001]. A less robust method, may fail when
      Cholesky is applied to singular input.

      `method="ortho"` - the LOBPCG method with orthogonal basis
      selection [StathopoulosEtal2002]. A robust method.

    Supported inputs are dense, sparse, and batches of dense matrices.

    .. note:: In general, the basic method spends least time per
      iteration. However, the robust methods converge much faster and
      are more stable. So, the usage of the basic method is generally
      not recommended but there exist cases where the usage of the
      basic method may be preferred.

    .. warning:: The backward method does not support sparse and complex inputs.
      It works only when `B` is not provided (i.e. `B == None`).
      We are actively working on extensions, and the details of
      the algorithms are going to be published promptly.

    .. warning:: While it is assumed that `A` is symmetric, `A.grad` is not.
      To make sure that `A.grad` is symmetric, so that `A - t * A.grad` is symmetric
      in first-order optimization routines, prior to running `lobpcg`
      we do the following symmetrization map: `A -> (A + A.t()) / 2`.
      The map is performed only when the `A` requires gradients.

    .. warning:: LOBPCG algorithm is not applicable when the number of `A`'s rows
      is smaller than 3x the number of requested eigenpairs `n`.

    Args:

      A (Tensor): the input tensor of size :math:`(*, m, m)`

      k (integer, optional): the number of requested
                  eigenpairs. Default is the number of :math:`X`
                  columns (when specified) or `1`.

      B (Tensor, optional): the input tensor of size :math:`(*, m,
                  m)`. When not specified, `B` is interpreted as
                  identity matrix.

      X (tensor, optional): the input tensor of size :math:`(*, m, n)`
                  where `k <= n <= m`. When specified, it is used as
                  initial approximation of eigenvectors. X must be a
                  dense tensor.

      n (integer, optional): if :math:`X` is not specified then `n`
                  specifies the size of the generated random
                  approximation of eigenvectors. Default value for `n`
                  is `k`. If :math:`X` is specified, any provided value of `n` is
                  ignored and `n` is automatically set to the number of
                  columns in :math:`X`.

      iK (tensor, optional): the input tensor of size :math:`(*, m,
                  m)`. When specified, it will be used as preconditioner.

      niter (int, optional): maximum number of iterations. When
                 reached, the iteration process is hard-stopped and
                 the current approximation of eigenpairs is returned.
                 For infinite iteration but until convergence criteria
                 is met, use `-1`.

      tol (float, optional): residual tolerance for stopping
                 criterion. Default is `feps ** 0.5` where `feps` is
                 smallest non-zero floating-point number of the given
                 input tensor `A` data type.

      largest (bool, optional): when True, solve the eigenproblem for
                 the largest eigenvalues. Otherwise, solve the
                 eigenproblem for smallest eigenvalues. Default is
                 `True`.

      method (str, optional): select LOBPCG method. See the
                 description of the function above. Default is
                 "ortho".

      tracker (callable, optional) : a function for tracing the
                 iteration process. When specified, it is called at
                 each iteration step with LOBPCG instance as an
                 argument. The LOBPCG instance holds the full state of
                 the iteration process in the following attributes:

                   `iparams`, `fparams`, `bparams` - dictionaries of
                   integer, float, and boolean valued input
                   parameters, respectively

                   `ivars`, `fvars`, `bvars`, `tvars` - dictionaries
                   of integer, float, boolean, and Tensor valued
                   iteration variables, respectively.

                   `A`, `B`, `iK` - input Tensor arguments.

                   `E`, `X`, `S`, `R` - iteration Tensor variables.

                 For instance:

                   `ivars["istep"]` - the current iteration step
                   `X` - the current approximation of eigenvectors
                   `E` - the current approximation of eigenvalues
                   `R` - the current residual
                   `ivars["converged_count"]` - the current number of converged eigenpairs
                   `tvars["rerr"]` - the current state of convergence criteria

                 Note that when `tracker` stores Tensor objects from
                 the LOBPCG instance, it must make copies of these.

                 If `tracker` sets `bvars["force_stop"] = True`, the
                 iteration process will be hard-stopped.

      ortho_iparams, ortho_fparams, ortho_bparams (dict, optional):
                 various parameters to LOBPCG algorithm when using
                 `method="ortho"`.

    Returns:

      E (Tensor): tensor of eigenvalues of size :math:`(*, k)`

      X (Tensor): tensor of eigenvectors of size :math:`(*, m, k)`

    References:

      [Knyazev2001] Andrew V. Knyazev. (2001) Toward the Optimal
      Preconditioned Eigensolver: Locally Optimal Block Preconditioned
      Conjugate Gradient Method. SIAM J. Sci. Comput., 23(2),
      517-541. (25 pages)
      https://epubs.siam.org/doi/abs/10.1137/S1064827500366124

      [StathopoulosEtal2002] Andreas Stathopoulos and Kesheng
      Wu. (2002) A Block Orthogonalization Procedure with Constant
      Synchronization Requirements. SIAM J. Sci. Comput., 23(6),
      2165-2182. (18 pages)
      https://epubs.siam.org/doi/10.1137/S1064827500370883

      [DuerschEtal2018] Jed A. Duersch, Meiyue Shao, Chao Yang, Ming
      Gu. (2018) A Robust and Efficient Implementation of LOBPCG.
      SIAM J. Sci. Comput., 40(5), C655-C676. (22 pages)
      https://arxiv.org/abs/1704.07458

    """

    if not torch.jit.is_scripting():
        tensor_ops = (A, B, X, iK)
        if not set(map(type, tensor_ops)).issubset(
            (torch.Tensor, type(None))
        ) and has_torch_function(tensor_ops):
            return handle_torch_function(
                lobpcg,
                tensor_ops,
                A,
                k=k,
                B=B,
                X=X,
                n=n,
                iK=iK,
                niter=niter,
                tol=tol,
                largest=largest,
                method=method,
                tracker=tracker,
                ortho_iparams=ortho_iparams,
                ortho_fparams=ortho_fparams,
                ortho_bparams=ortho_bparams,
            )

    if not torch._jit_internal.is_scripting():
        if A.requires_grad or (B is not None and B.requires_grad):
            # While it is expected that `A` is symmetric,
            # the `A_grad` might be not. Therefore we perform the trick below,
            # so that `A_grad` becomes symmetric.
            # The symmetrization is important for first-order optimization methods,
            # so that (A - alpha * A_grad) is still a symmetric matrix.
            # Same holds for `B`.
            A_sym = (A + A.mT) / 2
            B_sym = (B + B.mT) / 2 if (B is not None) else None

            return LOBPCGAutogradFunction.apply(
                A_sym,
                k,
                B_sym,
                X,
                n,
                iK,
                niter,
                tol,
                largest,
                method,
                tracker,
                ortho_iparams,
                ortho_fparams,
                ortho_bparams,
            )
    else:
        if A.requires_grad or (B is not None and B.requires_grad):
            raise RuntimeError(
                "Script and require grads is not supported atm."
                "If you just want to do the forward, use .detach()"
                "on A and B before calling into lobpcg"
            )

    return _lobpcg(
        A,
        k,
        B,
        X,
        n,
        iK,
        niter,
        tol,
        largest,
        method,
        tracker,
        ortho_iparams,
        ortho_fparams,
        ortho_bparams,
    )


def lobpcg(
    A,
    X,
    B=None,
    M=None,
    Y=None,
    tol=None,
    maxiter=None,
    largest=True,
    verbosityLevel=0,
    retLambdaHistory=False,
    retResidualNormsHistory=False,
    restartControl=20,
):
    """Locally Optimal Block Preconditioned Conjugate Gradient Method (LOBPCG).

    LOBPCG is a preconditioned eigensolver for large real symmetric and complex
    Hermitian definite generalized eigenproblems.

    Parameters
    ----------
    A : {sparse matrix, ndarray, LinearOperator, callable object}
        The Hermitian linear operator of the problem, usually given by a
        sparse matrix.  Often called the "stiffness matrix".
    X : ndarray, float32 or float64
        Initial approximation to the ``k`` eigenvectors (non-sparse).
        If `A` has ``shape=(n,n)`` then `X` must have ``shape=(n,k)``.
    B : {sparse matrix, ndarray, LinearOperator, callable object}
        Optional. By default ``B = None``, which is equivalent to identity.
        The right hand side operator in a generalized eigenproblem if present.
        Often called the "mass matrix". Must be Hermitian positive definite.
    M : {sparse matrix, ndarray, LinearOperator, callable object}
        Optional. By default ``M = None``, which is equivalent to identity.
        Preconditioner aiming to accelerate convergence.
    Y : ndarray, float32 or float64, default: None
        An ``n-by-sizeY`` ndarray of constraints with ``sizeY < n``.
        The iterations will be performed in the ``B``-orthogonal complement
        of the column-space of `Y`. `Y` must be full rank if present.
    tol : scalar, optional
        The default is ``tol=n*sqrt(eps)``.
        Solver tolerance for the stopping criterion.
    maxiter : int, default: 20
        Maximum number of iterations.
    largest : bool, default: True
        When True, solve for the largest eigenvalues, otherwise the smallest.
    verbosityLevel : int, optional
        By default ``verbosityLevel=0`` no output.
        Controls the solver standard/screen output.
    retLambdaHistory : bool, default: False
        Whether to return iterative eigenvalue history.
    retResidualNormsHistory : bool, default: False
        Whether to return iterative history of residual norms.
    restartControl : int, optional
        Iterations restart if the residuals jump ``2**restartControl`` times
        compared to the smallest recorded in ``retResidualNormsHistory``.
        The default is ``restartControl=20``, making the restarts rare for
        backward compatibility.

    Returns
    -------
    lambda : ndarray of the shape ``(k, )``.
        Array of ``k`` approximate eigenvalues.
    v : ndarray of the same shape as ``X.shape``.
        An array of ``k`` approximate eigenvectors.
    lambdaHistory : ndarray, optional.
        The eigenvalue history, if `retLambdaHistory` is ``True``.
    ResidualNormsHistory : ndarray, optional.
        The history of residual norms, if `retResidualNormsHistory`
        is ``True``.

    Notes
    -----
    The iterative loop runs ``maxit=maxiter`` (20 if ``maxit=None``)
    iterations at most and finishes earlier if the tolerance is met.
    Breaking backward compatibility with the previous version, LOBPCG
    now returns the block of iterative vectors with the best accuracy rather
    than the last one iterated, as a cure for possible divergence.

    If ``X.dtype == np.float32`` and user-provided operations/multiplications
    by `A`, `B`, and `M` all preserve the ``np.float32`` data type,
    all the calculations and the output are in ``np.float32``.

    The size of the iteration history output equals to the number of the best
    (limited by `maxit`) iterations plus 3: initial, final, and postprocessing.

    If both `retLambdaHistory` and `retResidualNormsHistory` are ``True``,
    the return tuple has the following format
    ``(lambda, V, lambda history, residual norms history)``.

    In the following ``n`` denotes the matrix size and ``k`` the number
    of required eigenvalues (smallest or largest).

    The LOBPCG code internally solves eigenproblems of the size ``3k`` on every
    iteration by calling the dense eigensolver `eigh`, so if ``k`` is not
    small enough compared to ``n``, it makes no sense to call the LOBPCG code.
    Moreover, if one calls the LOBPCG algorithm for ``5k > n``, it would likely
    break internally, so the code calls the standard function `eigh` instead.
    It is not that ``n`` should be large for the LOBPCG to work, but rather the
    ratio ``n / k`` should be large. It you call LOBPCG with ``k=1``
    and ``n=10``, it works though ``n`` is small. The method is intended
    for extremely large ``n / k``.

    The convergence speed depends basically on three factors:

    1. Quality of the initial approximations `X` to the seeking eigenvectors.
       Randomly distributed around the origin vectors work well if no better
       choice is known.

    2. Relative separation of the desired eigenvalues from the rest
       of the eigenvalues. One can vary ``k`` to improve the separation.

    3. Proper preconditioning to shrink the spectral spread.
       For example, a rod vibration test problem (under tests
       directory) is ill-conditioned for large ``n``, so convergence will be
       slow, unless efficient preconditioning is used. For this specific
       problem, a good simple preconditioner function would be a linear solve
       for `A`, which is easy to code since `A` is tridiagonal.

    References
    ----------
    .. [1] A. V. Knyazev (2001),
           Toward the Optimal Preconditioned Eigensolver: Locally Optimal
           Block Preconditioned Conjugate Gradient Method.
           SIAM Journal on Scientific Computing 23, no. 2,
           pp. 517-541. :doi:`10.1137/S1064827500366124`

    .. [2] A. V. Knyazev, I. Lashuk, M. E. Argentati, and E. Ovchinnikov
           (2007), Block Locally Optimal Preconditioned Eigenvalue Xolvers
           (BLOPEX) in hypre and PETSc. :arxiv:`0705.2626`

    .. [3] A. V. Knyazev's C and MATLAB implementations:
           https://github.com/lobpcg/blopex

    Examples
    --------
    Our first example is minimalistic - find the largest eigenvalue of
    a diagonal matrix by solving the non-generalized eigenvalue problem
    ``A x = lambda x`` without constraints or preconditioning.

    >>> import numpy as np
    >>> from scipy.sparse import diags_array
    >>> from scipy.sparse.linalg import LinearOperator, aslinearoperator
    >>> from scipy.sparse.linalg import lobpcg

    The square matrix size is

    >>> n = 100

    and its diagonal entries are 1, ..., 100 defined by

    >>> vals = np.arange(1, n + 1).astype(np.int16)

    The first mandatory input parameter in this test is
    the sparse diagonal matrix `A`
    of the eigenvalue problem ``A x = lambda x`` to solve.

    >>> A = diags_array(vals, offsets=0, shape=(n, n), dtype=None)
    >>> A.toarray()
    array([[  1,   0,   0, ...,   0,   0,   0],
           [  0,   2,   0, ...,   0,   0,   0],
           [  0,   0,   3, ...,   0,   0,   0],
           ...,
           [  0,   0,   0, ...,  98,   0,   0],
           [  0,   0,   0, ...,   0,  99,   0],
           [  0,   0,   0, ...,   0,   0, 100]], shape=(100, 100), dtype=int16)

    The second mandatory input parameter `X` is a 2D array with the
    row dimension determining the number of requested eigenvalues.
    `X` is an initial guess for targeted eigenvectors.
    `X` must have linearly independent columns.
    If no initial approximations available, randomly oriented vectors
    commonly work best, e.g., with components normally distributed
    around zero or uniformly distributed on the interval [-1 1].
    Setting the initial approximations to dtype ``np.float32``
    forces all iterative values to dtype ``np.float32`` speeding up
    the run while still allowing accurate eigenvalue computations.

    >>> k = 1
    >>> rng = np.random.default_rng()
    >>> X = rng.normal(size=(n, k))
    >>> X = X.astype(np.float32)

    >>> eigenvalues, _ = lobpcg(A, X, maxiter=60)
    >>> eigenvalues
    array([100.], dtype=float32)

    `lobpcg` needs only access the matrix product with `A` rather
    then the matrix itself. Since the matrix `A` is diagonal in
    this example, one can write a function of the matrix product
    ``A @ X`` using the diagonal values ``vals`` only, e.g., by
    element-wise multiplication with broadcasting in the lambda-function

    >>> A_lambda = lambda X: vals[:, np.newaxis] * X

    or the regular function

    >>> def A_matmat(X):
    ...     return vals[:, np.newaxis] * X

    and use the handle to one of these callables as an input

    >>> eigenvalues, _ = lobpcg(A_lambda, X, maxiter=60)
    >>> eigenvalues
    array([100.], dtype=float32)
    >>> eigenvalues, _ = lobpcg(A_matmat, X, maxiter=60)
    >>> eigenvalues
    array([100.], dtype=float32)

    The traditional callable `LinearOperator` is no longer
    necessary but still supported as the input to `lobpcg`.
    Specifying ``matmat=A_matmat`` explicitly improves performance. 

    >>> A_lo = LinearOperator((n, n), matvec=A_matmat, matmat=A_matmat, dtype=np.int16)
    >>> eigenvalues, _ = lobpcg(A_lo, X, maxiter=80)
    >>> eigenvalues
    array([100.], dtype=float32)

    The least efficient callable option is `aslinearoperator`:

    >>> eigenvalues, _ = lobpcg(aslinearoperator(A), X, maxiter=80)
    >>> eigenvalues
    array([100.], dtype=float32)

    We now switch to computing the three smallest eigenvalues specifying

    >>> k = 3
    >>> X = np.random.default_rng().normal(size=(n, k))

    and ``largest=False`` parameter

    >>> eigenvalues, _ = lobpcg(A, X, largest=False, maxiter=90)
    >>> print(eigenvalues)  
    [1. 2. 3.]

    The next example illustrates computing 3 smallest eigenvalues of
    the same matrix `A` given by the function handle ``A_matmat`` but
    with constraints and preconditioning.

    Constraints - an optional input parameter is a 2D array comprising
    of column vectors that the eigenvectors must be orthogonal to

    >>> Y = np.eye(n, 3)

    The preconditioner acts as the inverse of `A` in this example, but
    in the reduced precision ``np.float32`` even though the initial `X`
    and thus all iterates and the output are in full ``np.float64``.

    >>> inv_vals = 1./vals
    >>> inv_vals = inv_vals.astype(np.float32)
    >>> M = lambda X: inv_vals[:, np.newaxis] * X

    Let us now solve the eigenvalue problem for the matrix `A` first
    without preconditioning requesting 80 iterations

    >>> eigenvalues, _ = lobpcg(A_matmat, X, Y=Y, largest=False, maxiter=80)
    >>> eigenvalues
    array([4., 5., 6.])
    >>> eigenvalues.dtype
    dtype('float64')

    With preconditioning we need only 20 iterations from the same `X`

    >>> eigenvalues, _ = lobpcg(A_matmat, X, Y=Y, M=M, largest=False, maxiter=20)
    >>> eigenvalues
    array([4., 5., 6.])

    Note that the vectors passed in `Y` are the eigenvectors of the 3
    smallest eigenvalues. The results returned above are orthogonal to those.

    The primary matrix `A` may be indefinite, e.g., after shifting
    ``vals`` by 50 from 1, ..., 100 to -49, ..., 50, we still can compute
    the 3 smallest or largest eigenvalues.

    >>> vals = vals - 50
    >>> X = rng.normal(size=(n, k))
    >>> eigenvalues, _ = lobpcg(A_matmat, X, largest=False, maxiter=99)
    >>> eigenvalues
    array([-49., -48., -47.])
    >>> eigenvalues, _ = lobpcg(A_matmat, X, largest=True, maxiter=99)
    >>> eigenvalues
    array([50., 49., 48.])

    """
    blockVectorX = X
    bestblockVectorX = blockVectorX
    blockVectorY = Y
    residualTolerance = tol
    if maxiter is None:
        maxiter = 20

    bestIterationNumber = maxiter

    sizeY = 0
    if blockVectorY is not None:
        if len(blockVectorY.shape) != 2:
            warnings.warn(
                f"Expected rank-2 array for argument Y, instead got "
                f"{len(blockVectorY.shape)}, "
                f"so ignore it and use no constraints.",
                UserWarning, stacklevel=2
            )
            blockVectorY = None
        else:
            sizeY = blockVectorY.shape[1]

    # Block size.
    if blockVectorX is None:
        raise ValueError("The mandatory initial matrix X cannot be None")
    if len(blockVectorX.shape) != 2:
        raise ValueError("expected rank-2 array for argument X")

    n, sizeX = blockVectorX.shape

    # Data type of iterates, determined by X, must be inexact
    if not np.issubdtype(blockVectorX.dtype, np.inexact):
        warnings.warn(
            f"Data type for argument X is {blockVectorX.dtype}, "
            f"which is not inexact, so casted to np.float32.",
            UserWarning, stacklevel=2
        )
        blockVectorX = np.asarray(blockVectorX, dtype=np.float32)

    if retLambdaHistory:
        lambdaHistory = np.zeros((maxiter + 3, sizeX),
                                 dtype=blockVectorX.dtype)
    if retResidualNormsHistory:
        residualNormsHistory = np.zeros((maxiter + 3, sizeX),
                                        dtype=blockVectorX.dtype)

    if verbosityLevel:
        aux = "Solving "
        if B is None:
            aux += "standard"
        else:
            aux += "generalized"
        aux += " eigenvalue problem with"
        if M is None:
            aux += "out"
        aux += " preconditioning\n\n"
        aux += f"matrix size {n}\n"
        aux += f"block size {sizeX}\n\n"
        if blockVectorY is None:
            aux += "No constraints\n\n"
        else:
            if sizeY > 1:
                aux += f"{sizeY} constraints\n\n"
            else:
                aux += f"{sizeY} constraint\n\n"
        print(aux)

    if (n - sizeY) < (5 * sizeX):
        warnings.warn(
            f"The problem size {n} minus the constraints size {sizeY} "
            f"is too small relative to the block size {sizeX}. "
            f"Using a dense eigensolver instead of LOBPCG iterations."
            f"No output of the history of the iterations.",
            UserWarning, stacklevel=2
        )

        sizeX = min(sizeX, n)

        if blockVectorY is not None:
            raise NotImplementedError(
                "The dense eigensolver does not support constraints."
            )

        # Define the closed range of indices of eigenvalues to return.
        if largest:
            eigvals = (n - sizeX, n - 1)
        else:
            eigvals = (0, sizeX - 1)

        try:
            if isinstance(A, LinearOperator):
                A = A(np.eye(n, dtype=int))
            elif callable(A):
                A = A(np.eye(n, dtype=int))
                if A.shape != (n, n):
                    raise ValueError(
                        f"The shape {A.shape} of the primary matrix\n"
                        f"defined by a callable object is wrong.\n"
                        f"Expected {(n, n)}."
                    )
            elif issparse(A):
                A = A.toarray()
            else:
                A = np.asarray(A)
        except Exception as e:
            raise Exception(
                f"Primary MatMul call failed with error\n"
                f"{e}\n")

        if B is not None:
            try:
                if isinstance(B, LinearOperator):
                    B = B(np.eye(n, dtype=int))
                elif callable(B):
                    B = B(np.eye(n, dtype=int))
                    if B.shape != (n, n):
                        raise ValueError(
                            f"The shape {B.shape} of the secondary matrix\n"
                            f"defined by a callable object is wrong.\n"
                        )
                elif issparse(B):
                    B = B.toarray()
                else:
                    B = np.asarray(B)
            except Exception as e:
                raise Exception(
                    f"Secondary MatMul call failed with error\n"
                    f"{e}\n")

        try:
            vals, vecs = eigh(A,
                              B,
                              subset_by_index=eigvals,
                              check_finite=False)
            if largest:
                # Reverse order to be compatible with eigs() in 'LM' mode.
                vals = vals[::-1]
                vecs = vecs[:, ::-1]

            return vals, vecs
        except Exception as e:
            raise Exception(
                f"Dense eigensolver failed with error\n"
                f"{e}\n"
            )

    if (residualTolerance is None) or (residualTolerance <= 0.0):
        residualTolerance = np.sqrt(np.finfo(blockVectorX.dtype).eps) * n

    A = _makeMatMat(A)
    B = _makeMatMat(B)
    M = _makeMatMat(M)

    # Apply constraints to X.
    if blockVectorY is not None:

        if B is not None:
            blockVectorBY = B(blockVectorY)
            if blockVectorBY.shape != blockVectorY.shape:
                raise ValueError(
                    f"The shape {blockVectorY.shape} "
                    f"of the constraint not preserved\n"
                    f"and changed to {blockVectorBY.shape} "
                    f"after multiplying by the secondary matrix.\n"
                )
        else:
            blockVectorBY = blockVectorY

        # gramYBY is a dense array.
        gramYBY = blockVectorY.T.conj() @ blockVectorBY
        try:
            # gramYBY is a Cholesky factor from now on...
            gramYBY = cho_factor(gramYBY, overwrite_a=True)
        except LinAlgError as e:
            raise ValueError("Linearly dependent constraints") from e

        _applyConstraints(blockVectorX, gramYBY, blockVectorBY, blockVectorY)

    ##
    # B-orthonormalize X.
    blockVectorX, blockVectorBX, _ = _b_orthonormalize(
        B, blockVectorX, verbosityLevel=verbosityLevel)
    if blockVectorX is None:
        raise ValueError("Linearly dependent initial approximations")

    ##
    # Compute the initial Ritz vectors: solve the eigenproblem.
    blockVectorAX = A(blockVectorX)
    if blockVectorAX.shape != blockVectorX.shape:
        raise ValueError(
            f"The shape {blockVectorX.shape} "
            f"of the initial approximations not preserved\n"
            f"and changed to {blockVectorAX.shape} "
            f"after multiplying by the primary matrix.\n"
        )

    gramXAX = blockVectorX.T.conj() @ blockVectorAX

    _lambda, eigBlockVector = eigh(gramXAX, check_finite=False)
    ii = _get_indx(_lambda, sizeX, largest)
    _lambda = _lambda[ii]
    if retLambdaHistory:
        lambdaHistory[0, :] = _lambda

    eigBlockVector = np.asarray(eigBlockVector[:, ii])
    blockVectorX = _matmul_inplace(
        blockVectorX, eigBlockVector,
        verbosityLevel=verbosityLevel
    )
    blockVectorAX = _matmul_inplace(
        blockVectorAX, eigBlockVector,
        verbosityLevel=verbosityLevel
    )
    if B is not None:
        blockVectorBX = _matmul_inplace(
            blockVectorBX, eigBlockVector,
            verbosityLevel=verbosityLevel
        )

    ##
    # Active index set.
    activeMask = np.ones((sizeX,), dtype=bool)

    ##
    # Main iteration loop.

    blockVectorP = None  # set during iteration
    blockVectorAP = None
    blockVectorBP = None

    smallestResidualNorm = np.abs(np.finfo(blockVectorX.dtype).max)

    iterationNumber = -1
    restart = True
    forcedRestart = False
    explicitGramFlag = False
    while iterationNumber < maxiter:
        iterationNumber += 1

        if B is not None:
            aux = blockVectorBX * _lambda[np.newaxis, :]
        else:
            aux = blockVectorX * _lambda[np.newaxis, :]

        blockVectorR = blockVectorAX - aux

        aux = np.sum(blockVectorR.conj() * blockVectorR, 0)
        residualNorms = np.sqrt(np.abs(aux))
        if retResidualNormsHistory:
            residualNormsHistory[iterationNumber, :] = residualNorms
        residualNorm = np.sum(np.abs(residualNorms)) / sizeX

        if residualNorm < smallestResidualNorm:
            smallestResidualNorm = residualNorm
            bestIterationNumber = iterationNumber
            bestblockVectorX = blockVectorX
        elif residualNorm > 2**restartControl * smallestResidualNorm:
            forcedRestart = True
            blockVectorAX = A(blockVectorX)
            if blockVectorAX.shape != blockVectorX.shape:
                raise ValueError(
                    f"The shape {blockVectorX.shape} "
                    f"of the restarted iterate not preserved\n"
                    f"and changed to {blockVectorAX.shape} "
                    f"after multiplying by the primary matrix.\n"
                )
            if B is not None:
                blockVectorBX = B(blockVectorX)
                if blockVectorBX.shape != blockVectorX.shape:
                    raise ValueError(
                        f"The shape {blockVectorX.shape} "
                        f"of the restarted iterate not preserved\n"
                        f"and changed to {blockVectorBX.shape} "
                        f"after multiplying by the secondary matrix.\n"
                    )

        ii = np.where(residualNorms > residualTolerance, True, False)
        activeMask = activeMask & ii
        currentBlockSize = activeMask.sum()

        if verbosityLevel:
            print(f"iteration {iterationNumber}")
            print(f"current block size: {currentBlockSize}")
            print(f"eigenvalue(s):\n{_lambda}")
            print(f"residual norm(s):\n{residualNorms}")

        if currentBlockSize == 0:
            break

        activeBlockVectorR = _as2d(blockVectorR[:, activeMask])

        if iterationNumber > 0:
            activeBlockVectorP = _as2d(blockVectorP[:, activeMask])
            activeBlockVectorAP = _as2d(blockVectorAP[:, activeMask])
            if B is not None:
                activeBlockVectorBP = _as2d(blockVectorBP[:, activeMask])

        if M is not None:
            # Apply preconditioner T to the active residuals.
            activeBlockVectorR = M(activeBlockVectorR)

        ##
        # Apply constraints to the preconditioned residuals.
        if blockVectorY is not None:
            _applyConstraints(activeBlockVectorR,
                              gramYBY,
                              blockVectorBY,
                              blockVectorY)

        ##
        # B-orthogonalize the preconditioned residuals to X.
        if B is not None:
            activeBlockVectorR = activeBlockVectorR - (
                blockVectorX @
                (blockVectorBX.T.conj() @ activeBlockVectorR)
            )
        else:
            activeBlockVectorR = activeBlockVectorR - (
                blockVectorX @
                (blockVectorX.T.conj() @ activeBlockVectorR)
            )

        ##
        # B-orthonormalize the preconditioned residuals.
        aux = _b_orthonormalize(
            B, activeBlockVectorR, verbosityLevel=verbosityLevel)
        activeBlockVectorR, activeBlockVectorBR, _ = aux

        if activeBlockVectorR is None:
            warnings.warn(
                f"Failed at iteration {iterationNumber} with accuracies "
                f"{residualNorms}\n not reaching the requested "
                f"tolerance {residualTolerance}.",
                UserWarning, stacklevel=2
            )
            break
        activeBlockVectorAR = A(activeBlockVectorR)

        if iterationNumber > 0:
            if B is not None:
                aux = _b_orthonormalize(
                    B, activeBlockVectorP, activeBlockVectorBP,
                    verbosityLevel=verbosityLevel
                )
                activeBlockVectorP, activeBlockVectorBP, invR = aux
            else:
                aux = _b_orthonormalize(B, activeBlockVectorP,
                                        verbosityLevel=verbosityLevel)
                activeBlockVectorP, _, invR = aux
            # Function _b_orthonormalize returns None if Cholesky fails
            if activeBlockVectorP is not None:
                activeBlockVectorAP = _matmul_inplace(
                    activeBlockVectorAP, invR,
                    verbosityLevel=verbosityLevel
                )
                restart = forcedRestart
            else:
                restart = True

        ##
        # Perform the Rayleigh Ritz Procedure:
        # Compute symmetric Gram matrices:

        if activeBlockVectorAR.dtype == "float32":
            myeps = 1
        else:
            myeps = np.sqrt(np.finfo(activeBlockVectorR.dtype).eps)

        if residualNorms.max() > myeps and not explicitGramFlag:
            explicitGramFlag = False
        else:
            # Once explicitGramFlag, forever explicitGramFlag.
            explicitGramFlag = True

        # Shared memory assignments to simplify the code
        if B is None:
            blockVectorBX = blockVectorX
            activeBlockVectorBR = activeBlockVectorR
            if not restart:
                activeBlockVectorBP = activeBlockVectorP

        # Common submatrices:
        gramXAR = np.dot(blockVectorX.T.conj(), activeBlockVectorAR)
        gramRAR = np.dot(activeBlockVectorR.T.conj(), activeBlockVectorAR)

        gramDtype = activeBlockVectorAR.dtype
        if explicitGramFlag:
            gramRAR = (gramRAR + gramRAR.T.conj()) / 2
            gramXAX = np.dot(blockVectorX.T.conj(), blockVectorAX)
            gramXAX = (gramXAX + gramXAX.T.conj()) / 2
            gramXBX = np.dot(blockVectorX.T.conj(), blockVectorBX)
            gramRBR = np.dot(activeBlockVectorR.T.conj(), activeBlockVectorBR)
            gramXBR = np.dot(blockVectorX.T.conj(), activeBlockVectorBR)
        else:
            gramXAX = np.diag(_lambda).astype(gramDtype)
            gramXBX = np.eye(sizeX, dtype=gramDtype)
            gramRBR = np.eye(currentBlockSize, dtype=gramDtype)
            gramXBR = np.zeros((sizeX, currentBlockSize), dtype=gramDtype)

        if not restart:
            gramXAP = np.dot(blockVectorX.T.conj(), activeBlockVectorAP)
            gramRAP = np.dot(activeBlockVectorR.T.conj(), activeBlockVectorAP)
            gramPAP = np.dot(activeBlockVectorP.T.conj(), activeBlockVectorAP)
            gramXBP = np.dot(blockVectorX.T.conj(), activeBlockVectorBP)
            gramRBP = np.dot(activeBlockVectorR.T.conj(), activeBlockVectorBP)
            if explicitGramFlag:
                gramPAP = (gramPAP + gramPAP.T.conj()) / 2
                gramPBP = np.dot(activeBlockVectorP.T.conj(),
                                 activeBlockVectorBP)
            else:
                gramPBP = np.eye(currentBlockSize, dtype=gramDtype)

            gramA = np.block(
                [
                    [gramXAX, gramXAR, gramXAP],
                    [gramXAR.T.conj(), gramRAR, gramRAP],
                    [gramXAP.T.conj(), gramRAP.T.conj(), gramPAP],
                ]
            )
            gramB = np.block(
                [
                    [gramXBX, gramXBR, gramXBP],
                    [gramXBR.T.conj(), gramRBR, gramRBP],
                    [gramXBP.T.conj(), gramRBP.T.conj(), gramPBP],
                ]
            )

            _handle_gramA_gramB_verbosity(gramA, gramB, verbosityLevel)

            try:
                _lambda, eigBlockVector = eigh(gramA,
                                               gramB,
                                               check_finite=False)
            except LinAlgError as e:
                # raise ValueError("eigh failed in lobpcg iterations") from e
                if verbosityLevel:
                    warnings.warn(
                        f"eigh failed at iteration {iterationNumber} \n"
                        f"with error {e} causing a restart.\n",
                        UserWarning, stacklevel=2
                    )
                # try again after dropping the direction vectors P from RR
                restart = True

        if restart:
            gramA = np.block([[gramXAX, gramXAR], [gramXAR.T.conj(), gramRAR]])
            gramB = np.block([[gramXBX, gramXBR], [gramXBR.T.conj(), gramRBR]])

            _handle_gramA_gramB_verbosity(gramA, gramB, verbosityLevel)

            try:
                _lambda, eigBlockVector = eigh(gramA,
                                               gramB,
                                               check_finite=False)
            except LinAlgError as e:
                # raise ValueError("eigh failed in lobpcg iterations") from e
                warnings.warn(
                    f"eigh failed at iteration {iterationNumber} with error\n"
                    f"{e}\n",
                    UserWarning, stacklevel=2
                )
                break

        ii = _get_indx(_lambda, sizeX, largest)
        _lambda = _lambda[ii]
        eigBlockVector = eigBlockVector[:, ii]
        if retLambdaHistory:
            lambdaHistory[iterationNumber + 1, :] = _lambda

        # Compute Ritz vectors.
        if B is not None:
            if not restart:
                eigBlockVectorX = eigBlockVector[:sizeX]
                eigBlockVectorR = eigBlockVector[sizeX:
                                                 sizeX + currentBlockSize]
                eigBlockVectorP = eigBlockVector[sizeX + currentBlockSize:]

                pp = np.dot(activeBlockVectorR, eigBlockVectorR)
                pp += np.dot(activeBlockVectorP, eigBlockVectorP)

                app = np.dot(activeBlockVectorAR, eigBlockVectorR)
                app += np.dot(activeBlockVectorAP, eigBlockVectorP)

                bpp = np.dot(activeBlockVectorBR, eigBlockVectorR)
                bpp += np.dot(activeBlockVectorBP, eigBlockVectorP)
            else:
                eigBlockVectorX = eigBlockVector[:sizeX]
                eigBlockVectorR = eigBlockVector[sizeX:]

                pp = np.dot(activeBlockVectorR, eigBlockVectorR)
                app = np.dot(activeBlockVectorAR, eigBlockVectorR)
                bpp = np.dot(activeBlockVectorBR, eigBlockVectorR)

            blockVectorX = np.dot(blockVectorX, eigBlockVectorX) + pp
            blockVectorAX = np.dot(blockVectorAX, eigBlockVectorX) + app
            blockVectorBX = np.dot(blockVectorBX, eigBlockVectorX) + bpp

            blockVectorP, blockVectorAP, blockVectorBP = pp, app, bpp

        else:
            if not restart:
                eigBlockVectorX = eigBlockVector[:sizeX]
                eigBlockVectorR = eigBlockVector[sizeX:
                                                 sizeX + currentBlockSize]
                eigBlockVectorP = eigBlockVector[sizeX + currentBlockSize:]

                pp = np.dot(activeBlockVectorR, eigBlockVectorR)
                pp += np.dot(activeBlockVectorP, eigBlockVectorP)

                app = np.dot(activeBlockVectorAR, eigBlockVectorR)
                app += np.dot(activeBlockVectorAP, eigBlockVectorP)
            else:
                eigBlockVectorX = eigBlockVector[:sizeX]
                eigBlockVectorR = eigBlockVector[sizeX:]

                pp = np.dot(activeBlockVectorR, eigBlockVectorR)
                app = np.dot(activeBlockVectorAR, eigBlockVectorR)

            blockVectorX = np.dot(blockVectorX, eigBlockVectorX) + pp
            blockVectorAX = np.dot(blockVectorAX, eigBlockVectorX) + app

            blockVectorP, blockVectorAP = pp, app

    if B is not None:
        aux = blockVectorBX * _lambda[np.newaxis, :]
    else:
        aux = blockVectorX * _lambda[np.newaxis, :]

    blockVectorR = blockVectorAX - aux

    aux = np.sum(blockVectorR.conj() * blockVectorR, 0)
    residualNorms = np.sqrt(np.abs(aux))
    # Use old lambda in case of early loop exit.
    if retLambdaHistory:
        lambdaHistory[iterationNumber + 1, :] = _lambda
    if retResidualNormsHistory:
        residualNormsHistory[iterationNumber + 1, :] = residualNorms
    residualNorm = np.sum(np.abs(residualNorms)) / sizeX
    if residualNorm < smallestResidualNorm:
        smallestResidualNorm = residualNorm
        bestIterationNumber = iterationNumber + 1
        bestblockVectorX = blockVectorX

    if np.max(np.abs(residualNorms)) > residualTolerance:
        warnings.warn(
            f"Exited at iteration {iterationNumber} with accuracies \n"
            f"{residualNorms}\n"
            f"not reaching the requested tolerance {residualTolerance}.\n"
            f"Use iteration {bestIterationNumber} instead with accuracy \n"
            f"{smallestResidualNorm}.\n",
            UserWarning, stacklevel=2
        )

    if verbosityLevel:
        print(f"Final iterative eigenvalue(s):\n{_lambda}")
        print(f"Final iterative residual norm(s):\n{residualNorms}")

    blockVectorX = bestblockVectorX
    # Making eigenvectors "exactly" satisfy the blockVectorY constrains
    if blockVectorY is not None:
        _applyConstraints(blockVectorX,
                          gramYBY,
                          blockVectorBY,
                          blockVectorY)

    # Making eigenvectors "exactly" othonormalized by final "exact" RR
    blockVectorAX = A(blockVectorX)
    if blockVectorAX.shape != blockVectorX.shape:
        raise ValueError(
            f"The shape {blockVectorX.shape} "
            f"of the postprocessing iterate not preserved\n"
            f"and changed to {blockVectorAX.shape} "
            f"after multiplying by the primary matrix.\n"
        )
    gramXAX = np.dot(blockVectorX.T.conj(), blockVectorAX)

    blockVectorBX = blockVectorX
    if B is not None:
        blockVectorBX = B(blockVectorX)
        if blockVectorBX.shape != blockVectorX.shape:
            raise ValueError(
                f"The shape {blockVectorX.shape} "
                f"of the postprocessing iterate not preserved\n"
                f"and changed to {blockVectorBX.shape} "
                f"after multiplying by the secondary matrix.\n"
            )

    gramXBX = np.dot(blockVectorX.T.conj(), blockVectorBX)
    _handle_gramA_gramB_verbosity(gramXAX, gramXBX, verbosityLevel)
    gramXAX = (gramXAX + gramXAX.T.conj()) / 2
    gramXBX = (gramXBX + gramXBX.T.conj()) / 2
    try:
        _lambda, eigBlockVector = eigh(gramXAX,
                                       gramXBX,
                                       check_finite=False)
    except LinAlgError as e:
        raise ValueError("eigh has failed in lobpcg postprocessing") from e

    ii = _get_indx(_lambda, sizeX, largest)
    _lambda = _lambda[ii]
    eigBlockVector = np.asarray(eigBlockVector[:, ii])

    blockVectorX = np.dot(blockVectorX, eigBlockVector)
    blockVectorAX = np.dot(blockVectorAX, eigBlockVector)

    if B is not None:
        blockVectorBX = np.dot(blockVectorBX, eigBlockVector)
        aux = blockVectorBX * _lambda[np.newaxis, :]
    else:
        aux = blockVectorX * _lambda[np.newaxis, :]

    blockVectorR = blockVectorAX - aux

    aux = np.sum(blockVectorR.conj() * blockVectorR, 0)
    residualNorms = np.sqrt(np.abs(aux))

    if retLambdaHistory:
        lambdaHistory[bestIterationNumber + 1, :] = _lambda
    if retResidualNormsHistory:
        residualNormsHistory[bestIterationNumber + 1, :] = residualNorms

    if retLambdaHistory:
        lambdaHistory = lambdaHistory[
            : bestIterationNumber + 2, :]
    if retResidualNormsHistory:
        residualNormsHistory = residualNormsHistory[
            : bestIterationNumber + 2, :]

    if np.max(np.abs(residualNorms)) > residualTolerance:
        warnings.warn(
            f"Exited postprocessing with accuracies \n"
            f"{residualNorms}\n"
            f"not reaching the requested tolerance {residualTolerance}.",
            UserWarning, stacklevel=2
        )

    if verbosityLevel:
        print(f"Final postprocessing eigenvalue(s):\n{_lambda}")
        print(f"Final residual norm(s):\n{residualNorms}")

    if retLambdaHistory:
        lambdaHistory = np.vsplit(lambdaHistory, np.shape(lambdaHistory)[0])
        lambdaHistory = [np.squeeze(i) for i in lambdaHistory]
    if retResidualNormsHistory:
        residualNormsHistory = np.vsplit(residualNormsHistory,
                                         np.shape(residualNormsHistory)[0])
        residualNormsHistory = [np.squeeze(i) for i in residualNormsHistory]

    if retLambdaHistory:
        if retResidualNormsHistory:
            return _lambda, blockVectorX, lambdaHistory, residualNormsHistory
        else:
            return _lambda, blockVectorX, lambdaHistory
    else:
        if retResidualNormsHistory:
            return _lambda, blockVectorX, residualNormsHistory
        else:
            return _lambda, blockVectorX

