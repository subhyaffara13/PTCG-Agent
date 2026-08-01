
def _lu_solve(lu, piv, b, trans, overwrite_b, check_finite):
    if check_finite:
        b1 = asarray_chkfinite(b)
    else:
        b1 = asarray(b)

    _deprecate_dtypes("lu_solve", lu, b)

    overwrite_b = overwrite_b or _datacopied(b1, b)

    if lu.shape[0] != b1.shape[0]:
        raise ValueError(f"Shapes of lu {lu.shape} and b {b1.shape} are incompatible")

    # accommodate empty arrays
    if b1.size == 0:
        m = lu_solve((np.eye(2, dtype=lu.dtype), [0, 1]), np.ones(2, dtype=b.dtype))
        return np.empty_like(b1, dtype=m.dtype)

    getrs, = get_lapack_funcs(('getrs',), (lu, b1))
    x, info = getrs(lu, piv, b1, trans=trans, overwrite_b=overwrite_b)
    if info == 0:
        return x
    raise ValueError(f'illegal value in {-info}th argument of internal gesv|posv')


def _lu_solve(lu: Array, permutation: Array, b: Array, trans: int) -> Array:
  if len(lu.shape) < 2 or lu.shape[-1] != lu.shape[-2]:
    raise ValueError("last two dimensions of LU decomposition must be equal, "
                     "got shape {}".format(lu.shape))
  if len(b.shape) < 1:
    raise ValueError("b matrix must have rank >= 1, got shape {}"
                     .format(b.shape))
  # Broadcasting follows NumPy's convention for linalg.solve: the RHS is
  # treated as a (batched) vector if the number of dimensions differ by 1.
  # Otherwise, broadcasting rules apply.
  rhs_vector = lu.ndim == b.ndim + 1
  if rhs_vector:
    if b.shape[-1] != lu.shape[-1]:
      raise ValueError("When LU decomposition matrix and b have the same "
                       "number of dimensions, last axis of LU decomposition "
                       "matrix (shape {}) and b array (shape {}) must match"
                       .format(lu.shape, b.shape))
    b = b[..., np.newaxis]
  else:
    if b.shape[-2] != lu.shape[-1]:
      raise ValueError("When LU decomposition matrix and b different "
                       "numbers of dimensions, last axis of LU decomposition "
                       "matrix (shape {}) and second to last axis of b array "
                       "(shape {}) must match"
                       .format(lu.shape, b.shape))

  batch_shape = lax.broadcast_shapes(lu.shape[:-2], permutation.shape[:-1], b.shape[:-2])
  lu = _broadcast_to(lu, (*batch_shape, *lu.shape[-2:]))
  permutation = _broadcast_to(permutation, (*batch_shape, permutation.shape[-1]))
  b = _broadcast_to(b, (*batch_shape, *b.shape[-2:]))
  fn = _lu_solve_core
  for _ in batch_shape:
    fn = api.vmap(fn, in_axes=(0, 0, 0, None))
  x = fn(lu, permutation, b, trans)
  return x[..., 0] if rhs_vector else x

