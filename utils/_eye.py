
def _eye(m, n, k, dtype, format, as_sparray=True):
    if as_sparray:
        csr_sparse = csr_array
        csc_sparse = csc_array
        coo_sparse = coo_array
        diags_sparse = diags_array
    else:
        csr_sparse = csr_matrix
        csc_sparse = csc_matrix
        coo_sparse = coo_matrix
        diags_sparse = diags

    if n is None:
        n = m
    m, n = int(m), int(n)

    if m == n and k == 0:
        # fast branch for special formats
        if format in ['csr', 'csc']:
            idx_dtype = get_index_dtype(maxval=n)
            indptr = np.arange(n+1, dtype=idx_dtype)
            indices = np.arange(n, dtype=idx_dtype)
            data = np.ones(n, dtype=dtype)
            cls = {'csr': csr_sparse, 'csc': csc_sparse}[format]
            return cls((data, indices, indptr), (n, n))

        elif format == 'coo':
            idx_dtype = get_index_dtype(maxval=n)
            row = np.arange(n, dtype=idx_dtype)
            col = np.arange(n, dtype=idx_dtype)
            data = np.ones(n, dtype=dtype)
            return coo_sparse((data, (row, col)), (n, n))

    data = np.ones((1, max(0, min(m + k, n))), dtype=dtype)
    return diags_sparse(data, offsets=[k], shape=(m, n), dtype=dtype).asformat(format)


def _eye(dtype: DTypeLike, shape: Shape, offset: DimSize = 0) -> Array:
  """Like numpy.eye, create a 2D array with ones on a diagonal."""
  offset = _clip_int_to_valid_range(offset, np.int32,
                                    "argument `offset` of jax.numpy.eye")
  dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "eye")
  bool_eye = eq(add(broadcasted_iota(np.int32, shape, 0), np.int32(offset)),
                broadcasted_iota(np.int32, shape, 1))
  return convert_element_type_p.bind(bool_eye, new_dtype=dtype, weak_type=False,
                                     sharding=None)


def _eye(N: DimSize, M: DimSize | None = None,
        k: int | ArrayLike = 0,
        dtype: DTypeLike | None = None) -> Array:
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype, "eye")
  if isinstance(k, int):
    k = lax._clip_int_to_valid_range(k, np.int32,
                                              "`argument `k` of jax.numpy.eye")
  offset = util.ensure_arraylike("eye", k)
  if not (offset.shape == () and dtypes.issubdtype(offset.dtype, np.integer)):
    raise ValueError(f"k must be a scalar integer; got {k}")
  N_int = core.canonicalize_dim(N, "argument of 'N' jnp.eye()")
  M_int = N_int if M is None else core.canonicalize_dim(M, "argument 'M' of jnp.eye()")
  if N_int < 0 or M_int < 0:
    raise ValueError(f"negative dimensions are not allowed, got {N} and {M}")
  i = lax.broadcasted_iota(offset.dtype, (N_int, M_int), 0)
  j = lax.broadcasted_iota(offset.dtype, (N_int, M_int), 1)
  return (i + offset == j).astype(dtype)

