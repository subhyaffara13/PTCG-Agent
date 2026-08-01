
def _eigh_work(H, n, termination_size, subset_by_index):
  """ The main work loop performing the symmetric eigendecomposition of H.
  Each step recursively computes a projector into the space of eigenvalues
  above jnp.mean(jnp.diag(H)). The result of the projections into and out of
  that space, along with the isometries accomplishing these, are then computed.
  This is performed recursively until the projections have size 1, and thus
  store an eigenvalue of the original input; the corresponding isometry is
  the related eigenvector. The results are then composed.

  This function cannot be Jitted because the internal split_spectrum cannot
  be.

  Args:
    H: The Hermitian input.
    n: The true (dynamic) shape of H.

  Returns:
    H, V: The result of the projection.
  """
  # We turn what was originally a recursive algorithm into an iterative
  # algorithm with an explicit stack.
  N, _ = H.shape
  n = jnp.asarray(n, np.int32)
  agenda = Stack.create(
    N + 1, _Subproblem(jnp.array(0, np.int32), jnp.array(0, np.int32)))
  agenda = agenda.push(_Subproblem(offset=jnp.array(0, np.int32), size=n))

  # eigenvectors is the array in which we build the output eigenvectors.
  # We initialize it with the identity matrix so the initial matrix
  # multiplications in_split_spectrum_jittable are the identity.
  eigenvectors = jnp.eye(N, dtype=H.dtype)

  # Keep a copy of the initial matrix Frobenius norm, so we know when to stop
  # recursing. When the sub-matrix norm is less than eps*H0_norm, the contents are
  # pure numerical noise, and we should just stop.
  H0_norm = jnp_linalg.norm(_mask(H, (n, n)))

  # blocks is an array representing a stack of Hermitian matrix blocks that we
  # need to recursively decompose. Subproblems are different sizes, so the stack
  # of blocks is ragged. Subproblems are left-aligned (i.e. starting at the 0th
  # column). Here is an ASCII art picture of three blocks A, B, C, embedded
  # in the larger `blocks` workspace (represented with trailing dots).
  #
  # A A A . . .
  # A A A . . .
  # A A A . . .
  # B B . . . .
  # B B . . . .
  # C C C C . .
  # C C C C . .
  # C C C C . .
  # C C C C . .
  #
  # Each step of the algorithm subdivides a block into two subblocks whose
  # sizes sum to the original block size. We overwrite the original block with
  # those two subblocks so we don't need any additional scratch space.
  #
  # At termination, "blocks" will contain 1x1 blocks (i.e., the eigenvalues) in
  # its first column.
  blocks = H

  def base_case(B, offset, b, agenda, blocks, eigenvectors):
    # Base case: for blocks under a minimum size, we cutoff the recursion
    # and call the TPU Jacobi eigendecomposition implementation. The Jacobi
    # algorithm works well for small matrices but scales poorly, so the two
    # complement each other well.
    H = _slice(blocks, (offset, 0), (b, b), (B, B))
    V = _slice(eigenvectors, (0, offset), (n, b), (N, B))

    # We replace the masked-out part of the matrix with the identity matrix.
    # We know that the TPU Jacobi eigh implementation will not alter the order
    # of the eigenvalues, so we know the eigendecomposition of the original
    # matrix is in the top-left corner of the eigendecomposition of the padded
    # matrix.
    # It is very important that the underlying eigh implementation does not sort
    # the eigenvalues for this reason! This is currently not true of JAX's CPU
    # and GPU eigendecompositions, and for those platforms this algorithm will
    # only do the right thing if termination_size == 1.
    H = _mask(H, (b, b))
    eig_vecs, eig_vals = lax_linalg.eigh(H, sort_eigenvalues=False)
    eig_vecs = _mask(eig_vecs, (b, b))
    eig_vals = _mask(eig_vals, (b,))
    eig_vecs = tensor_contractions.dot(V, eig_vecs)

    eig_vals = eig_vals.astype(eig_vecs.dtype)
    blocks = _update_slice(blocks, eig_vals[:, None], (offset, 0), (b, 1))
    eigenvectors = _update_slice(eigenvectors, eig_vecs, (0, offset), (n, b))
    return agenda, blocks, eigenvectors

  def recursive_case(B, offset, b, agenda, blocks, eigenvectors):
    # The recursive case of the algorithm, specialized to a static block size
    # of B.
    H = _slice(blocks, (offset, 0), (b, b), (B, B))

    def nearly_diagonal_case(agenda, blocks, eigenvectors):
      blocks = _update_slice(blocks, jnp.diag(H)[:, None], (offset, 0), (b, 1))
      return agenda, blocks, eigenvectors

    def should_update_range(start, end, subset_by_index):
      return (
          True
          if subset_by_index is None
          else ((start < subset_by_index[1]) & (end > subset_by_index[0]))
      )

    def default_case(agenda, blocks, eigenvectors):
      V = _slice(eigenvectors, (0, offset), (n, b), (N, B))
      # TODO: Improve this?
      split_point = reductions.nanmedian(_mask(jnp.diag(ufuncs.real(H)), (b,), np.nan))
      H_minus, V_minus, H_plus, V_plus, rank = split_spectrum(
          H, b, split_point, V0=V)

      # Update state for *_minus.
      updated_minus_state = (
          _update_slice(blocks, H_minus, (offset, 0), (rank, rank)),
          _update_slice(eigenvectors, V_minus, (0, offset), (n, rank)),
          agenda.push(_Subproblem(offset, rank)),
      )
      should_update_minus = should_update_range(
          offset, offset + rank, subset_by_index
      )
      blocks, eigenvectors, agenda = lax.cond(
          should_update_minus,
          lambda: updated_minus_state,
          lambda: (blocks, eigenvectors, agenda),
      )

      # Update state for *_plus.
      updated_plus_state = (
          _update_slice(
              blocks, H_plus, (offset + rank, 0), (b - rank, b - rank)
          ),
          _update_slice(
              eigenvectors, V_plus, (0, offset + rank), (n, b - rank)
          ),
          agenda.push(_Subproblem(offset + rank, (b - rank))),
      )

      should_update_plus = should_update_range(
          offset + rank, offset + b, subset_by_index
      )
      blocks, eigenvectors, agenda = lax.cond(
          should_update_plus,
          lambda: updated_plus_state,
          lambda: (blocks, eigenvectors, agenda),
      )

      return agenda, blocks, eigenvectors

    # If the matrix is nearly diagonal or has a tiny Frobenius norm compared to
    # the original input matrix,, terminate the execution. This is necessary to
    # handle matrices with clusters of eigenvalues, including rank deficient
    # matrices. See Nakatsukasa and Higham section 5.2.
    norm = jnp_linalg.norm(H)
    eps = jnp.asarray(dtypes.finfo(H.dtype).eps, dtype=norm.dtype)
    off_diag_norm = jnp_linalg.norm(
        H - jnp.diag(jnp.diag(ufuncs.real(H)).astype(H.dtype)))
    nearly_diagonal = off_diag_norm <= 5 * eps * norm
    tiny = norm < eps * H0_norm
    return lax.cond(
        nearly_diagonal | tiny,
        nearly_diagonal_case,
        default_case,
        agenda,
        blocks,
        eigenvectors,
    )

  def loop_cond(state):
    agenda, _, _ = state
    return ~agenda.empty()

  # It would be wasteful to perform all computation padded up to the original
  # matrix size. Instead, we form buckets of padded sizes e.g.,
  # [N_0, N_1, ... N_k], aiming for a balance between compilation time
  # and runtime.
  cutoff = min(N, termination_size)
  buckets = [cutoff]
  branches = [partial(base_case, cutoff)]
  if N > termination_size:
    # If N > termination_size  We use the following schedule:
    #   1. N_0 = N,
    #   2. N_i = _round_up(int(N_{i-1} / 1.98), 32), 0 < i < k
    #   3. N_k = termination_size
    # the rule for N_i is to avoid falling into the original large bucket
    # when not splitting exactly at the half-way point during the recursion.
    buckets.append(N)
    branches.append(partial(recursive_case, N))
    multiplier = 1.98
    granularity = 32
    i = int(N / multiplier)
    while i > cutoff:
      bucket_size = _round_up(i, granularity)
      buckets.append(bucket_size)
      branches.append(partial(recursive_case, bucket_size))
      i = i // 2
  buckets_arr = jnp.array(buckets, dtype=np.int32)

  def loop_body(state):
    agenda, blocks, eigenvectors = state
    (offset, b), agenda = agenda.pop()
    which = jnp.where(buckets_arr < b, dtypes.iinfo(np.int32).max, buckets_arr)
    choice = jnp.argmin(which)
    return lax.switch(choice, branches, offset, b, agenda, blocks, eigenvectors)

  _, blocks, eigenvectors = lax.while_loop(
      loop_cond, loop_body, (agenda, blocks, eigenvectors))
  return blocks[:, 0], eigenvectors

