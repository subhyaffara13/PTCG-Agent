
def kron(a: ArrayLike, b: ArrayLike):
    return torch.kron(a, b)


def kron(A, B, format=None):
    """Sparse representation of the Kronecker product of `A` and `B`.

    Computes the Kronecker product, a composite sparse array
    made of blocks consisting of the second input array multiplied
    by each element of the first input array.

    .. warning::

        `kron` is switching to the sparse array interface.

        For the case where no input arrays are sparse, this function is
        switching to returning a sparse array instead of sparse matrix.
        Control the sparse return class by making at least one input sparse,
        e.g., ``kron(coo_matrix(A), B)``, or ``kron(coo_array(A), B)``.
        That removes any deprecation warnings as well.
        For more general information about sparrays, see
        :ref:`Migration from spmatrix to sparray <migration_to_sparray>`.
        Handling of this no sparse input case will change no earlier than v1.20.

    Parameters
    ----------
    A : sparse or dense array
        first array of the product
    B : sparse or dense array
        second array of the product
    format : str, optional (default: 'bsr' or 'coo')
        format of the result (e.g. "csr")
        If None, choose 'bsr' for relatively dense 2D arrays and 'coo' for others

    Returns
    -------
    sparse matrix or array
        kronecker product in a sparse format. Returns a sparse matrix unless either
        `A` or `B` is a sparse array in which case returns a sparse array.

    Examples
    --------
    >>> import numpy as np
    >>> import scipy as sp
    >>> A = sp.sparse.csr_array(np.array([[0, 2], [5, 0]]))
    >>> B = sp.sparse.csr_array(np.array([[1, 2], [3, 4]]))
    >>> sp.sparse.kron(A, B).toarray()
    array([[ 0,  0,  2,  4],
           [ 0,  0,  6,  8],
           [ 5, 10,  0,  0],
           [15, 20,  0,  0]])

    >>> sp.sparse.kron(A, [[1, 2], [3, 4]]).toarray()
    array([[ 0,  0,  2,  4],
           [ 0,  0,  6,  8],
           [ 5, 10,  0,  0],
           [15, 20,  0,  0]])

    """
    # TODO: delete this if-clause and replace _sparse with _array when spmatrix removed
    if isinstance(A, sparray) or isinstance(B, sparray):
        # convert to local variables
        bsr_sparse = bsr_array
        csr_sparse = csr_array
        coo_sparse = coo_array
    elif isinstance(A, spmatrix) or isinstance(B, spmatrix):
        bsr_sparse = bsr_matrix
        csr_sparse = csr_matrix
        coo_sparse = coo_matrix
    else:  # all dense
        msg = """`kron` is switching to the sparse array interface.

        For the case where input arrays are numpy arrays, this function is
        switching to returning a sparse array instead of sparse matrix.
        Recover the sparse matrix return value by making one input a sparse matrix.
        For example, kron(coo_matrix(A), B).
        Avoid this message for sparse array output by using kron(coo_array(A), B).
        For more information, see the spmatrix to sparray migration guide
        https://docs.scipy.org/doc/scipy/reference/sparse.migration_to_sparray.html

        This function will be changed no earlier than v1.20.
        """
        prefixes = (os.path.dirname(__file__),)
        warn(msg, category=DeprecationWarning, skip_file_prefixes=prefixes)
        # default when all input are ndarray
        bsr_sparse = bsr_matrix
        csr_sparse = csr_matrix
        coo_sparse = coo_matrix

    B = coo_sparse(B)

    # B is 2D and fairly dense, and format aligns with bsr, compute using BSR
    if (
        (format is None or format == "bsr") and
        B.ndim == 2 and 2*B.nnz >= math.prod(B.shape)
    ):
        if not hasattr(A, 'ndim') or A.ndim != 2:
            # CSR routes thru COO in constructor so can make COO to check ndim
            A = coo_sparse(A)
        if A.ndim == 2:
            A = csr_sparse(A, copy=True)
            output_shape = (A.shape[0]*B.shape[0], A.shape[1]*B.shape[1])

            if A.nnz == 0 or B.nnz == 0:
                # kronecker product is the zero matrix
                return coo_sparse(output_shape).asformat(format)

            B = B.toarray()
            data = A.data.repeat(B.size).reshape(-1, B.shape[0], B.shape[1])
            data = data * B

            return bsr_sparse((data, A.indices, A.indptr), shape=output_shape)
    else:
        A = coo_sparse(A)  # no copy needed as we use np.repeat below

    # compute using COO (convert to desired format just before return)
    if coo_sparse is coo_matrix:
        output_shape = (A.shape[0] * B.shape[0], A.shape[1] * B.shape[1])
        ndim_diff = 0
    else:
        ndim_diff = A.ndim - B.ndim
        A_shape = A.shape if ndim_diff >= 0 else (1,) * (-ndim_diff) + A.shape
        B_shape = B.shape if ndim_diff <= 0 else (1,) * ndim_diff + B.shape
        output_shape = tuple(a * b for a, b in zip(A_shape, B_shape))

    if A.nnz == 0 or B.nnz == 0:
        # kronecker product is the zero matrix
        return coo_sparse(output_shape).asformat(format)

    # expand entries of a into blocks
    data = A.data.repeat(B.nnz)
    idx_dtype = get_index_dtype(A.coords, maxval=max(output_shape))
    coords = [np.asarray(co, dtype=idx_dtype).repeat(B.nnz) for co in A.coords]
    if ndim_diff < 0:
        new_co = np.zeros_like(coords[0])
        coords = [new_co] + [new_co.copy() for _ in range(-ndim_diff - 1)] + coords

    # The last B.ndim coords need to be updated. Any previous columns in B are from
    # prepending (1,)s, so coord from A is what we need (B coord axis is all 0)
    for co, B_shape_i in zip(coords[-B.ndim:], B.shape):
        co *= B_shape_i

    # increment block indices
    coords[-B.ndim:] = [(co.reshape(-1, B.nnz) + Bco).ravel()
                        for co, Bco in zip(coords[-B.ndim:], B.coords)]
    # compute block entries
    data = (data.reshape(-1, B.nnz) * B.data).ravel()

    return coo_sparse((data, tuple(coords)), shape=output_shape).asformat(format)


def kron(
    a: Array | complex,
    b: Array | complex,
    /,
    *,
    xp: ModuleType | None = None,
) -> Array:
    """
    Kronecker product of two arrays.

    Computes the Kronecker product, a composite array made of blocks of the
    second array scaled by the first.

    Equivalent to ``numpy.kron`` for NumPy arrays.

    Parameters
    ----------
    a, b : Array | int | float | complex
        Input arrays or scalars. At least one must be an array.
    xp : array_namespace, optional
        The standard-compatible namespace for `a` and `b`. Default: infer.

    Returns
    -------
    array
        The Kronecker product of `a` and `b`.

    Notes
    -----
    The function assumes that the number of dimensions of `a` and `b`
    are the same, if necessary prepending the smallest with ones.
    If ``a.shape = (r0,r1,..,rN)`` and ``b.shape = (s0,s1,...,sN)``,
    the Kronecker product has shape ``(r0*s0, r1*s1, ..., rN*SN)``.
    The elements are products of elements from `a` and `b`, organized
    explicitly by::

        kron(a,b)[k0,k1,...,kN] = a[i0,i1,...,iN] * b[j0,j1,...,jN]

    where::

        kt = it * st + jt,  t = 0,...,N

    In the common 2-D case (N=1), the block structure can be visualized::

        [[ a[0,0]*b,   a[0,1]*b,  ... , a[0,-1]*b  ],
         [  ...                              ...   ],
         [ a[-1,0]*b,  a[-1,1]*b, ... , a[-1,-1]*b ]]

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> xpx.kron(xp.asarray([1, 10, 100]), xp.asarray([5, 6, 7]), xp=xp)
    Array([  5,   6,   7,  50,  60,  70, 500,
           600, 700], dtype=array_api_strict.int64)

    >>> xpx.kron(xp.asarray([5, 6, 7]), xp.asarray([1, 10, 100]), xp=xp)
    Array([  5,  50, 500,   6,  60, 600,   7,
            70, 700], dtype=array_api_strict.int64)

    >>> xpx.kron(xp.eye(2), xp.ones((2, 2)), xp=xp)
    Array([[1., 1., 0., 0.],
           [1., 1., 0., 0.],
           [0., 0., 1., 1.],
           [0., 0., 1., 1.]], dtype=array_api_strict.float64)

    >>> a = xp.reshape(xp.arange(100), (2, 5, 2, 5))
    >>> b = xp.reshape(xp.arange(24), (2, 3, 4))
    >>> c = xpx.kron(a, b, xp=xp)
    >>> c.shape
    (2, 10, 6, 20)
    >>> I = (1, 3, 0, 2)
    >>> J = (0, 2, 1)
    >>> J1 = (0,) + J             # extend to ndim=4
    >>> S1 = (1,) + b.shape
    >>> K = tuple(xp.asarray(I) * xp.asarray(S1) + xp.asarray(J1))
    >>> c[K] == a[I]*b[J]
    Array(True, dtype=array_api_strict.bool)
    """
    if xp is None:
        xp = array_namespace(a, b)
    a, b = asarrays(a, b, xp=xp)

    singletons = (1,) * (b.ndim - a.ndim)
    a = cast(Array, xp.broadcast_to(a, singletons + a.shape))

    nd_b, nd_a = b.ndim, a.ndim
    nd_max = max(nd_b, nd_a)
    if nd_a == 0 or nd_b == 0:
        return xp.multiply(a, b)

    a_shape = eager_shape(a)
    b_shape = eager_shape(b)

    # Equalise the shapes by prepending smaller one with 1s
    a_shape = (1,) * max(0, nd_b - nd_a) + a_shape
    b_shape = (1,) * max(0, nd_a - nd_b) + b_shape

    # Insert empty dimensions
    a_arr = expand_dims(a, axis=tuple(range(nd_b - nd_a)), xp=xp)
    b_arr = expand_dims(b, axis=tuple(range(nd_a - nd_b)), xp=xp)

    # Compute the product
    a_arr = expand_dims(a_arr, axis=tuple(range(1, nd_max * 2, 2)), xp=xp)
    b_arr = expand_dims(b_arr, axis=tuple(range(0, nd_max * 2, 2)), xp=xp)
    result = xp.multiply(a_arr, b_arr)

    # Reshape back and return
    res_shape = tuple(a_s * b_s for a_s, b_s in zip(a_shape, b_shape, strict=True))
    return xp.reshape(result, res_shape)


def kron(a, b):
    """
    Kronecker product of two arrays.

    Computes the Kronecker product, a composite array made of blocks of the
    second array scaled by the first.

    Parameters
    ----------
    a, b : array_like

    Returns
    -------
    out : ndarray

    See Also
    --------
    outer : The outer product

    Notes
    -----
    The function assumes that the number of dimensions of `a` and `b`
    are the same, if necessary prepending the smallest with ones.
    If ``a.shape = (r0,r1,...,rN)`` and ``b.shape = (s0,s1,...,sN)``,
    the Kronecker product has shape ``(r0*s0, r1*s1, ..., rN*SN)``.
    The elements are products of elements from `a` and `b`, organized
    explicitly by::

        kron(a,b)[k0,k1,...,kN] = a[i0,i1,...,iN] * b[j0,j1,...,jN]

    where::

        kt = it * st + jt,  t = 0,...,N

    In the common 2-D case (N=1), the block structure can be visualized::

        [[ a[0,0]*b,   a[0,1]*b,  ... , a[0,-1]*b  ],
         [  ...                              ...   ],
         [ a[-1,0]*b,  a[-1,1]*b, ... , a[-1,-1]*b ]]


    Examples
    --------
    >>> import numpy as np
    >>> np.kron([1,10,100], [5,6,7])
    array([  5,   6,   7, ..., 500, 600, 700])
    >>> np.kron([5,6,7], [1,10,100])
    array([  5,  50, 500, ...,   7,  70, 700])

    >>> np.kron(np.eye(2), np.ones((2,2)))
    array([[1.,  1.,  0.,  0.],
           [1.,  1.,  0.,  0.],
           [0.,  0.,  1.,  1.],
           [0.,  0.,  1.,  1.]])

    >>> a = np.arange(100).reshape((2,5,2,5))
    >>> b = np.arange(24).reshape((2,3,4))
    >>> c = np.kron(a,b)
    >>> c.shape
    (2, 10, 6, 20)
    >>> I = (1,3,0,2)
    >>> J = (0,2,1)
    >>> J1 = (0,) + J             # extend to ndim=4
    >>> S1 = (1,) + b.shape
    >>> K = tuple(np.array(I) * np.array(S1) + np.array(J1))
    >>> c[K] == a[I]*b[J]
    True

    """
    # Working:
    # 1. Equalise the shapes by prepending smaller array with 1s
    # 2. Expand shapes of both the arrays by adding new axes at
    #    odd positions for 1st array and even positions for 2nd
    # 3. Compute the product of the modified array
    # 4. The inner most array elements now contain the rows of
    #    the Kronecker product
    # 5. Reshape the result to kron's shape, which is same as
    #    product of shapes of the two arrays.
    b = asanyarray(b)
    a = array(a, copy=None, subok=True, ndmin=b.ndim)
    is_any_mat = isinstance(a, matrix) or isinstance(b, matrix)
    ndb, nda = b.ndim, a.ndim
    nd = max(ndb, nda)

    if (nda == 0 or ndb == 0):
        return _nx.multiply(a, b)

    as_ = a.shape
    bs = b.shape
    if not a.flags.contiguous:
        a = reshape(a, as_)
    if not b.flags.contiguous:
        b = reshape(b, bs)

    # Equalise the shapes by prepending smaller one with 1s
    as_ = (1,) * max(0, ndb - nda) + as_
    bs = (1,) * max(0, nda - ndb) + bs

    # Insert empty dimensions
    a_arr = expand_dims(a, axis=tuple(range(ndb - nda)))
    b_arr = expand_dims(b, axis=tuple(range(nda - ndb)))

    # Compute the product
    a_arr = expand_dims(a_arr, axis=tuple(range(1, nd * 2, 2)))
    b_arr = expand_dims(b_arr, axis=tuple(range(0, nd * 2, 2)))
    # In case of `mat`, convert result to `array`
    result = _nx.multiply(a_arr, b_arr, subok=(not is_any_mat))

    # Reshape back
    result = result.reshape(_nx.multiply(as_, bs))

    return result if not is_any_mat else matrix(result, copy=False)


def kron(a: ArrayLike, b: ArrayLike) -> Array:
  """Compute the Kronecker product of two input arrays.

  JAX implementation of :func:`numpy.kron`.

  The Kronecker product is an operation on two matrices of arbitrary size that
  produces a block matrix. Each element of the first matrix ``a`` is multiplied by
  the entire second matrix ``b``. If ``a`` has shape (m, n) and ``b``
  has shape (p, q), the resulting matrix will have shape (m * p, n * q).

  Args:
    a: first input array with any shape.
    b: second input array with any shape.

  Returns:
    A new array representing the Kronecker product of the inputs  ``a`` and ``b``.
    The shape of the output is the element-wise product of the input shapes.

  See also:
    - :func:`jax.numpy.outer`: compute the outer product of two arrays.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([[5, 6],
    ...                [7, 8]])
    >>> jnp.kron(a, b)
    Array([[ 5,  6, 10, 12],
           [ 7,  8, 14, 16],
           [15, 18, 20, 24],
           [21, 24, 28, 32]], dtype=int32)
  """
  util.check_arraylike("kron", a, b)
  a, b = util.promote_dtypes(a, b)
  if np.ndim(a) < np.ndim(b):
    a = expand_dims(a, range(np.ndim(b) - np.ndim(a)))
  elif np.ndim(b) < np.ndim(a):
    b = expand_dims(b, range(np.ndim(a) - np.ndim(b)))
  a_reshaped = expand_dims(a, range(1, 2 * np.ndim(a), 2))
  b_reshaped = expand_dims(b, range(0, 2 * np.ndim(b), 2))
  out_shape = tuple(np.multiply(np.shape(a), np.shape(b)))
  return reshape(lax.mul(a_reshaped, b_reshaped), out_shape)

