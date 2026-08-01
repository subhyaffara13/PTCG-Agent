
def eigh_tridiagonal(d, e, eigvals_only=False, select='a', select_range=None,
                     check_finite=True, tol=0., lapack_driver='auto'):
    """
    Solve eigenvalue problem for a real symmetric tridiagonal matrix.

    Find eigenvalues `w` and optionally right eigenvectors `v` of ``a``::

        a v[:,i] = w[i] v[:,i]
        v.H v    = identity

    For a real symmetric matrix ``a`` with diagonal elements `d` and
    off-diagonal elements `e`.

    Parameters
    ----------
    d : ndarray, shape (ndim,)
        The diagonal elements of the array.
    e : ndarray, shape (ndim-1,)
        The off-diagonal elements of the array.
    eigvals_only : bool, optional
        Compute only the eigenvalues and no eigenvectors.
        (Default: calculate also eigenvectors)
    select : {'a', 'v', 'i'}, optional
        Which eigenvalues to calculate

        ======  ========================================
        select  calculated
        ======  ========================================
        'a'     All eigenvalues
        'v'     Eigenvalues in the interval (min, max]
        'i'     Eigenvalues with indices min <= i <= max
        ======  ========================================
    select_range : (min, max), optional
        Range of selected eigenvalues
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    tol : float
        The absolute tolerance to which each eigenvalue is required
        (only used when 'stebz' is the `lapack_driver`).
        An eigenvalue (or cluster) is considered to have converged if it
        lies in an interval of this width. If <= 0. (default),
        the value ``eps*|a|`` is used where eps is the machine precision,
        and ``|a|`` is the 1-norm of the matrix ``a``.
    lapack_driver : str
        LAPACK function to use, can be 'auto', 'stemr', 'stebz', 'sterf',
        'stev', or 'stevd'. When 'auto' (default), it will use 'stevd' if ``select='a'``
        and 'stebz' otherwise. When 'stebz' is used to find the eigenvalues and
        ``eigvals_only=False``, then a second LAPACK call (to ``?STEIN``) is
        used to find the corresponding eigenvectors. 'sterf' can only be
        used when ``eigvals_only=True`` and ``select='a'``. 'stev' can only
        be used when ``select='a'``.

    Returns
    -------
    w : (M,) ndarray
        The eigenvalues, in ascending order, each repeated according to its
        multiplicity.
    v : (M, M) ndarray
        The normalized eigenvector corresponding to the eigenvalue ``w[i]`` is
        the column ``v[:,i]``. Only returned if ``eigvals_only=False``.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge.

    See Also
    --------
    eigvalsh_tridiagonal : eigenvalues of symmetric/Hermitian tridiagonal
        matrices
    eig : eigenvalues and right eigenvectors for non-symmetric arrays
    eigh : eigenvalues and right eigenvectors for symmetric/Hermitian arrays
    eig_banded : eigenvalues and right eigenvectors for symmetric/Hermitian
        band matrices

    Notes
    -----
    This function makes use of LAPACK ``S/DSTEMR`` routines.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import eigh_tridiagonal
    >>> d = 3*np.ones(4)
    >>> e = -1*np.ones(3)
    >>> w, v = eigh_tridiagonal(d, e)
    >>> A = np.diag(d) + np.diag(e, k=1) + np.diag(e, k=-1)
    >>> np.allclose(A @ v - v @ np.diag(w), np.zeros((4, 4)))
    True
    """
    d = _asarray_validated(d, check_finite=check_finite)
    e = _asarray_validated(e, check_finite=check_finite)
    for check in (d, e):
        if check.ndim != 1:
            raise ValueError('expected a 1-D array')
        if check.dtype.char in 'GFD':  # complex
            raise TypeError('Only real arrays currently supported')
    if d.size != e.size + 1:
        raise ValueError(f'd ({d.size}) must have one more element than e ({e.size})')
    select, vl, vu, il, iu, _ = _check_select(
        select, select_range, 0, d.size)
    if not isinstance(lapack_driver, str):
        raise TypeError('lapack_driver must be str')
    drivers = ('auto', 'stemr', 'sterf', 'stebz', 'stev', 'stevd')
    if lapack_driver not in drivers:
        raise ValueError(f'lapack_driver must be one of {drivers}, '
                         f'got {lapack_driver}')
    if lapack_driver == 'auto':
        lapack_driver = 'stevd' if select == 0 else 'stebz'

    # Quick exit for 1x1 case
    if len(d) == 1:
        if select == 1 and (not (vl < d[0] <= vu)):  # request by value
            w = array([])
            v = empty([1, 0], dtype=d.dtype)
        else:  # all and request by index
            w = array([d[0]], dtype=d.dtype)
            v = array([[1.]], dtype=d.dtype)

        if eigvals_only:
            return w
        else:
            return w, v

    func, = get_lapack_funcs((lapack_driver,), (d, e))
    compute_v = not eigvals_only
    if lapack_driver == 'sterf':
        if select != 0:
            raise ValueError('sterf can only be used when select == "a"')
        if not eigvals_only:
            raise ValueError('sterf can only be used when eigvals_only is '
                             'True')
        w, info = func(d, e)
        m = len(w)
    elif lapack_driver == 'stev':
        if select != 0:
            raise ValueError('stev can only be used when select == "a"')
        w, v, info = func(d, e, compute_v=compute_v)
        m = len(w)
    elif lapack_driver == 'stevd':
        if select != 0:
            raise ValueError('stevd can only be used when select == "a"')
        w, v, info = func(d, e, compute_v=compute_v)
        m = len(w)
    elif lapack_driver == 'stebz':
        tol = float(tol)
        internal_name = 'stebz'
        stebz, = get_lapack_funcs((internal_name,), (d, e))
        # If getting eigenvectors, needs to be block-ordered (B) instead of
        # matrix-ordered (E), and we will reorder later
        order = 'E' if eigvals_only else 'B'
        m, w, iblock, isplit, info = stebz(d, e, select, vl, vu, il, iu, tol,
                                           order)
    else:   # 'stemr'
        # ?STEMR annoyingly requires size N instead of N-1
        e_ = empty(e.size+1, e.dtype)
        e_[:-1] = e
        stemr_lwork, = get_lapack_funcs(('stemr_lwork',), (d, e))
        lwork, liwork, info = stemr_lwork(d, e_, select, vl, vu, il, iu,
                                          compute_v=compute_v)
        _check_info(info, 'stemr_lwork')
        m, w, v, info = func(d, e_, select, vl, vu, il, iu,
                             compute_v=compute_v, lwork=lwork, liwork=liwork)
    _check_info(info, lapack_driver + ' (eigh_tridiagonal)')
    w = w[:m]
    if eigvals_only:
        return w
    else:
        # Do we still need to compute the eigenvalues?
        if lapack_driver == 'stebz':
            func, = get_lapack_funcs(('stein',), (d, e))
            v, info = func(d, e, w, iblock, isplit)
            _check_info(info, 'stein (eigh_tridiagonal)',
                        positive='%d eigenvectors failed to converge')
            # Convert block-order to matrix-order
            order = argsort(w)
            w, v = w[order], v[:, order]
        else:
            v = v[:, :m]
        return w, v


def eigh_tridiagonal(d: ArrayLike, e: ArrayLike, *, eigvals_only: bool = False,
                     select: str = 'a', select_range: tuple[float, float] | None = None,
                     tol: float | None = None,
                     key: Array | None = None) -> Array | tuple[Array, Array]:
  """Solve the eigenvalue problem for a symmetric real tridiagonal matrix

  JAX implementation of :func:`scipy.linalg.eigh_tridiagonal`.

  Args:
    d: real-valued array of shape ``(N,)`` specifying the diagonal elements.
    e: real-valued array of shape ``(N - 1,)`` specifying the off-diagonal elements.
    eigvals_only: If True, return only the eigenvalues (default: False). Computation
      of eigenvectors is not yet implemented, so ``eigvals_only`` must be set to True.
    select: specify which eigenvalues to calculate. Supported values are:

      - ``'a'``: all eigenvalues
      - ``'i'``: eigenvalues with indices ``select_range[0] <= i <= select_range[1]``

      JAX does not currently implement ``select = 'v'``.
    select_range: range of values used when ``select='i'``.
    tol: absolute tolerance to use when solving for the eigenvalues.
    key: a PRNG key, as returned by ``jax.random.key``, used to generate random
      initialization vectors for inverse iteration. If ``None``, defaults to a
      fixed PRNG key.

  Returns:
    An array of eigenvalues with shape ``(N,)``.

  See also:
    :func:`jax.scipy.linalg.eigh`: general Hermitian eigenvalue solver

  Examples:
    >>> d = jnp.array([1., 2., 3., 4.])
    >>> e = jnp.array([1., 1., 1.])
    >>> eigvals = jax.scipy.linalg.eigh_tridiagonal(d, e, eigvals_only=True)
    >>> eigvals
    Array([0.2547188, 1.8227171, 3.1772828, 4.745281 ], dtype=float32)

    For comparison, we can construct the full matrix and compute the same result
    using :func:`~jax.scipy.linalg.eigh`:

    >>> A = jnp.diag(d) + jnp.diag(e, 1) + jnp.diag(e, -1)
    >>> A
    Array([[1., 1., 0., 0.],
           [1., 2., 1., 0.],
           [0., 1., 3., 1.],
           [0., 0., 1., 4.]], dtype=float32)
    >>> eigvals_full = jax.scipy.linalg.eigh(A, eigvals_only=True)
    >>> jnp.allclose(eigvals, eigvals_full)
    Array(True, dtype=bool)
  """
  if not eigvals_only and key is None:
    key = random.key(42)

  def _sturm(alpha, beta_sq, pivmin, alpha0_perturbation, x):
    """Implements the Sturm sequence recurrence."""
    n = alpha.shape[0]
    zeros = jnp.zeros(x.shape, dtype=np.int32)
    ones = jnp.ones(x.shape, dtype=np.int32)

    # The first step in the Sturm sequence recurrence
    # requires special care if x is equal to alpha[0].
    def sturm_step0():
      q = alpha[0] - x
      count = jnp.where(q < 0, ones, zeros)
      q = jnp.where(alpha[0] == x, alpha0_perturbation, q)
      return q, count

    # Subsequent steps all take this form:
    def sturm_step(i, q, count):
      q = alpha[i] - beta_sq[i - 1] / q - x
      count = jnp.where(q <= pivmin, count + 1, count)
      q = jnp.where(q <= pivmin, jnp.minimum(q, -pivmin), q)
      return q, count

    # The first step initializes q and count.
    q, count = sturm_step0()

    # Peel off ((n-1) % blocksize) steps from the main loop, so we can run
    # the bulk of the iterations unrolled by a factor of blocksize.
    blocksize = 16
    i = 1
    peel = (n - 1) % blocksize
    unroll_cnt = peel

    def unrolled_steps(args):
      start, q, count = args
      for j in range(unroll_cnt):
        q, count = sturm_step(start + j, q, count)
      return start + unroll_cnt, q, count

    i, q, count = unrolled_steps((i, q, count))

    # Run the remaining steps of the Sturm sequence using a partially
    # unrolled while loop.
    unroll_cnt = blocksize
    def cond(iqc):
      i, q, count = iqc
      return jnp.less(i, n)
    _, _, count = lax.while_loop(cond, unrolled_steps, (i, q, count))
    return count

  alpha = jnp.asarray(d)
  beta = jnp.asarray(e)
  supported_dtypes = (np.float32, np.float64, np.complex64, np.complex128)
  if alpha.dtype != beta.dtype:
    raise TypeError("diagonal and off-diagonal values must have same dtype, "
                    f"got {alpha.dtype} and {beta.dtype}")
  if alpha.dtype not in supported_dtypes or beta.dtype not in supported_dtypes:
    raise TypeError("Only float32 and float64 inputs are supported as inputs "
                    "to jax.scipy.linalg.eigh_tridiagonal, got "
                    f"{alpha.dtype} and {beta.dtype}")
  n = alpha.shape[0]
  if n <= 1:
    if eigvals_only:
      return jnp.real(alpha)
    else:
      return jnp.real(alpha), jnp.eye(n, dtype=alpha.dtype)

  if dtypes.issubdtype(alpha.dtype, np.complexfloating):
    alpha = jnp.real(alpha)
    beta_sq = jnp.real(beta * jnp.conj(beta))
    beta_abs = jnp.sqrt(beta_sq)
  else:
    beta_abs = jnp.abs(beta)
    beta_sq = jnp.square(beta)

  # Estimate the largest and smallest eigenvalues of T using the Gershgorin
  # circle theorem.
  off_diag_abs_row_sum = jnp.concatenate(
      [beta_abs[:1], beta_abs[:-1] + beta_abs[1:], beta_abs[-1:]], axis=0)
  lambda_est_max = jnp.amax(alpha + off_diag_abs_row_sum)
  lambda_est_min = jnp.amin(alpha - off_diag_abs_row_sum)
  # Upper bound on 2-norm of T.
  t_norm = jnp.maximum(jnp.abs(lambda_est_min), jnp.abs(lambda_est_max))

  # Compute the smallest allowed pivot in the Sturm sequence to avoid
  # overflow.
  finfo = np.finfo(alpha.dtype)
  one = np.ones([], dtype=alpha.dtype)
  safemin = np.maximum(one / finfo.max, (one + finfo.eps) * finfo.tiny)
  pivmin = safemin * jnp.maximum(1, jnp.amax(beta_sq))
  alpha0_perturbation = jnp.square(finfo.eps * beta_abs[0])
  abs_tol = finfo.eps * t_norm
  if tol is not None:
    abs_tol = jnp.maximum(tol, abs_tol)

  # In the worst case, when the absolute tolerance is eps*lambda_est_max and
  # lambda_est_max = -lambda_est_min, we have to take as many bisection steps
  # as there are bits in the mantissa plus 1.
  # The proof is left as an exercise to the reader.
  max_it = finfo.nmant + 1

  # Determine the indices of the desired eigenvalues, based on select and
  # select_range.
  if select == 'a':
    target_counts = jnp.arange(n, dtype=np.int32)
  elif select == 'i':
    if select_range is None:
      raise ValueError("for select='i', select_range must be specified.")
    if select_range[0] > select_range[1]:
      raise ValueError('Got empty index range in select_range.')
    target_counts = jnp.arange(select_range[0], select_range[1] + 1, dtype=np.int32)
  elif select == 'v':
    # TODO(phawkins): requires dynamic shape support.
    raise NotImplementedError("eigh_tridiagonal(..., select='v') is not "
                              "implemented")
  else:
    raise ValueError("'select must have a value in {'a', 'i', 'v'}.")

  # Run binary search for all desired eigenvalues in parallel, starting from
  # the interval lightly wider than the estimated
  # [lambda_est_min, lambda_est_max].
  fudge = 2.1  # We widen starting interval the Gershgorin interval a bit.
  norm_slack = jnp.array(n, alpha.dtype) * fudge * finfo.eps * t_norm
  lower = lambda_est_min - norm_slack - 2 * fudge * pivmin
  upper = lambda_est_max + norm_slack + fudge * pivmin

  # Pre-broadcast the scalars used in the Sturm sequence for improved
  # performance.
  target_shape = np.shape(target_counts)
  lower = jnp.broadcast_to(lower, shape=target_shape)
  upper = jnp.broadcast_to(upper, shape=target_shape)
  mid = 0.5 * (upper + lower)
  pivmin = jnp.broadcast_to(pivmin, target_shape)
  alpha0_perturbation = jnp.broadcast_to(alpha0_perturbation, target_shape)

  # Start parallel binary searches.
  def cond(args):
    i, lower, _, upper = args
    return jnp.logical_and(
        jnp.less(i, max_it),
        jnp.less(abs_tol, jnp.amax(upper - lower)))

  def body(args):
    i, lower, mid, upper = args
    counts = _sturm(alpha, beta_sq, pivmin, alpha0_perturbation, mid)
    lower = jnp.where(counts <= target_counts, mid, lower)
    upper = jnp.where(counts > target_counts, mid, upper)
    mid = 0.5 * (lower + upper)
    return i + 1, lower, mid, upper

  def _compute_eigenvectors(alpha, beta, eigvals, key):
    """Implements inverse iteration to compute eigenvectors."""
    n = alpha.shape[0]
    k = eigvals.shape[0]

    # Pad beta to length n
    dl = jnp.pad(jnp.conj(beta), (1, 0))
    du = jnp.pad(beta, (0, 1))

    # Eigenvectors corresponding to cluster of close eigenvalues are
    # not unique and need to be explicitly orthogonalized. Here we
    # identify such clusters. Note: This function assumes that
    # eigenvalues are sorted in non-decreasing order.
    gap = eigvals[1:] - eigvals[:-1]
    eps = np.finfo(eigvals.dtype).eps
    t_norm = jnp.maximum(jnp.abs(eigvals[0]), jnp.abs(eigvals[-1]))
    gaptol = jnp.sqrt(eps) * t_norm

    # Find the beginning and end of runs of eigenvectors corresponding
    # to eigenvalues closer than "gaptol", which will need to be
    # orthogonalized against each other.
    close = gap < gaptol
    left_neighbor_close = jnp.pad(close, (1, 0), constant_values=False)
    right_neighbor_close = jnp.pad(close, (0, 1), constant_values=False)

    ortho_interval_start = jnp.logical_and(
        jnp.logical_not(left_neighbor_close), right_neighbor_close)
    ortho_interval_end = jnp.logical_and(
        left_neighbor_close, jnp.logical_not(right_neighbor_close))

    max_clusters = k // 2 + 1
    starts = jnp.nonzero(ortho_interval_start, size=max_clusters)[0]
    ends = jnp.nonzero(ortho_interval_end, size=max_clusters)[0] + 1
    num_clusters = jnp.sum(ortho_interval_start)

    arange_k = jnp.arange(k)

    solve_dtype = np.result_type(alpha.dtype, beta.dtype)
    base_dtype = np.finfo(solve_dtype).dtype
    # We perform inverse iteration for all eigenvectors in parallel,
    # starting from a random set of vectors, until all have converged.
    v = random.normal(key, (k, n), dtype=base_dtype).astype(solve_dtype)
    v = v / jnp.linalg.norm(v, axis=-1, keepdims=True).astype(solve_dtype)


    def orthogonalize_close_eigenvectors(ev):
      # Eigenvectors corresponding to a cluster of close eigenvalues are not
      # uniquely defined, but the subspace they span is. To avoid numerical
      # instability, we explicitly mutually orthogonalize such eigenvectors
      # after each step of inverse iteration. It is customary to use
      # modified Gram-Schmidt for this, but this is not very efficient
      # on some platforms, so here we defer to the QR decomposition in JAX.
      def orthogonalize_cluster(i, ev):
        start = starts[i]
        end = ends[i]
        c = end - start

        ev_padded = jnp.pad(ev, ((0, k), (0, 0)))
        v_block = lax.dynamic_slice(ev_padded, (start, 0), (k, n))

        mask = (arange_k < c).astype(ev.dtype)
        v_block_masked = v_block * mask[:, None]

        # We use the builtin QR factorization to orthonormalize the
        # vectors in the cluster.
        Q, _ = jnp_linalg.qr(v_block_masked.T)

        QT = Q.T
        QT_masked = QT * mask[:, None]

        big_zeros = jnp.zeros((2 * k, n), dtype=ev.dtype)
        big_update = lax.dynamic_update_slice(big_zeros, QT_masked, (start, 0))
        update_full = big_update[:k, :]

        is_in_cluster = (arange_k >= start) & (arange_k < end)
        ev = jnp.where(is_in_cluster[:, None], update_full, ev)

        return ev

      ev = lax.fori_loop(0, num_clusters, orthogonalize_cluster, ev)
      return ev

    # Replicate alpha-shifted and beta across the k eigenvectors so we
    # can solve the k systems
    #    [T - eigvals(i)*eye(n)] x_i = r_i
    # simultaneously using the batching mechanism.
    alpha_shifted = alpha[None, :] - eigvals[:, None]
    dl_batched = jnp.broadcast_to(dl[None, :], (k, n))
    du_batched = jnp.broadcast_to(du[None, :], (k, n))

    def inverse_iteration_step(state):
      i, v, nrm_v, nrm_v_old = state

      v_new = lax_linalg.tridiagonal_solve(
          dl_batched.astype(solve_dtype),
          alpha_shifted.astype(solve_dtype),
          du_batched.astype(solve_dtype),
          v[:, :, None].astype(solve_dtype),
          perturb_singular=True)
      v_new = jnp.squeeze(v_new, axis=-1)

      nrm_v_new = jnp.linalg.norm(v_new, axis=-1, keepdims=True)
      v_new = v_new / nrm_v_new.astype(v_new.dtype)
      nrm_v_new = jnp.squeeze(nrm_v_new, axis=-1)

      v_new = orthogonalize_close_eigenvectors(v_new)

      return i + 1, v_new, nrm_v_new, nrm_v

    def continue_iteration(state):
      i, _, nrm_v, nrm_v_old = state
      max_it = 5  # Taken from LAPACK xSTEIN.
      min_norm_growth = 0.1
      norm_growth_factor = 1 + min_norm_growth
      # We stop the inverse iteration when we reach the maximum number of
      # iterations or the norm growths is less than 10%.
      return jnp.logical_and(
          i < max_it,
          jnp.any(nrm_v >= norm_growth_factor * nrm_v_old)
      )

    _, v_final, _, _ = lax.while_loop(
        continue_iteration,
        inverse_iteration_step,
        (0, v, jnp.ones(k, dtype=eigvals.dtype), jnp.zeros(k, dtype=eigvals.dtype))
    )

    return v_final

  _, _, mid, _ = lax.while_loop(cond, body, (0, lower, mid, upper))

  if eigvals_only:
    return mid

  eigenvectors = _compute_eigenvectors(alpha, beta, mid, key)
  return mid, eigenvectors.T

