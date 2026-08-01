
def matrix_norm(
    A: TensorLikeType,
    ord: float | str = "fro",
    dim: DimsType = (-2, -1),
    keepdim: bool = False,
    *,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    # shape
    check_is_matrix(A, "linalg.matrix_norm")
    # dim

    dim = utils.canonicalize_dims(A.ndim, dim)
    if isinstance(dim, Dim):
        dim = (dim,)  # type: ignore[assignment]
    torch._check(
        len(dim) == 2, lambda: f"linalg.matrix_norm: dim must be a 2-tuple. Got {dim}"
    )
    torch._check(
        # pyrefly: ignore [bad-index]
        dim[0] != dim[1],
        # pyrefly: ignore [bad-index, index-error]
        # pyrefly: ignore [bad-index, index-error]
        lambda: f"linalg.matrix_norm: dims must be different. Got ({dim[0]}, {dim[1]})",
    )
    # dtype arg
    _check_norm_dtype(dtype, A.dtype, "linalg.matrix_norm")

    if isinstance(ord, str):
        # ord
        torch._check(
            ord in ("fro", "nuc"),
            lambda: f"linalg.matrix_norm: Order {ord} not supported.",
        )
        # dtype
        check_fp_or_complex(
            A.dtype, "linalg.matrix_norm", allow_low_precision_dtypes=ord != "nuc"
        )

        if ord == "fro":
            return vector_norm(A, 2, dim, keepdim, dtype=dtype)
        else:  # ord == "nuc"
            if dtype is not None:
                A = _maybe_convert_to_dtype(A, dtype)  # type: ignore[assignment]
            # pyrefly: ignore [bad-index, index-error]
            perm = _backshift_permutation(dim[0], dim[1], A.ndim)
            result = torch.sum(svdvals(prims.transpose(A, perm)), -1, keepdim)
            if keepdim:
                inv_perm = _inverse_permutation(perm)
                result = prims.transpose(torch.unsqueeze(result, -1), inv_perm)
            return result
    else:
        # ord
        abs_ord = abs(ord)
        torch._check(
            abs_ord in (2, 1, float("inf")),
            lambda: f"linalg.matrix_norm: Order {ord} not supported.",
        )
        # dtype
        check_fp_or_complex(
            A.dtype, "linalg.matrix_norm", allow_low_precision_dtypes=ord != 2
        )

        max_min = partial(torch.amax if ord > 0.0 else torch.amin, keepdim=keepdim)

        def _max_min_wrapper(A, dim):
            # pyrefly: ignore [unsupported-operation]
            if A.size(dim) == 0 and ord > 0.0:
                new_size = list(A.size())
                if keepdim:
                    new_size[dim] = 1
                else:
                    del new_size[dim]
                return torch.zeros(new_size, dtype=A.dtype, device=A.device)
            else:
                return max_min(A, dim)

        if abs_ord == 2.0:
            if dtype is not None:
                A = _maybe_convert_to_dtype(A, dtype)  # type: ignore[assignment]
            # pyrefly: ignore [bad-index, index-error]
            perm = _backshift_permutation(dim[0], dim[1], A.ndim)
            result = _max_min_wrapper(svdvals(prims.transpose(A, perm)), dim=-1)
            if keepdim:
                inv_perm = _inverse_permutation(perm)
                result = prims.transpose(torch.unsqueeze(result, -1), inv_perm)
            return result
        else:  # 1, -1, inf, -inf
            # pyrefly: ignore [bad-unpacking]
            dim0, dim1 = dim
            if abs_ord == float("inf"):
                dim0, dim1 = dim1, dim0
            if not keepdim and (dim0 < dim1):
                dim1 -= 1
            return _max_min_wrapper(
                vector_norm(A, 1.0, dim=dim0, keepdim=keepdim, dtype=dtype), dim1
            )


def matrix_norm(
    x: Array,
    /,
    xp: Namespace,
    *,
    keepdims: bool = False,
    ord: Literal[1, 2, -1, -2] | JustFloat | Literal["fro", "nuc"] | None = "fro",
) -> Array:
    return xp.linalg.norm(x, axis=(-2, -1), keepdims=keepdims, ord=ord)


def matrix_norm(x, /, *, keepdims=False, ord="fro"):
    """
    Computes the matrix norm of a matrix (or a stack of matrices) ``x``.

    This function is Array API compatible.

    Parameters
    ----------
    x : array_like
        Input array having shape (..., M, N) and whose two innermost
        dimensions form ``MxN`` matrices.
    keepdims : bool, optional
        If this is set to True, the axes which are normed over are left in
        the result as dimensions with size one. Default: False.
    ord : {1, -1, 2, -2, inf, -inf, 'fro', 'nuc'}, optional
        The order of the norm. For details see the table under ``Notes``
        in `numpy.linalg.norm`.

    See Also
    --------
    numpy.linalg.norm : Generic norm function

    Examples
    --------
    >>> from numpy import linalg as LA
    >>> a = np.arange(9) - 4
    >>> a
    array([-4, -3, -2, ...,  2,  3,  4])
    >>> b = a.reshape((3, 3))
    >>> b
    array([[-4, -3, -2],
           [-1,  0,  1],
           [ 2,  3,  4]])

    >>> LA.matrix_norm(b)
    7.745966692414834
    >>> LA.matrix_norm(b, ord='fro')
    7.745966692414834
    >>> LA.matrix_norm(b, ord=np.inf)
    9.0
    >>> LA.matrix_norm(b, ord=-np.inf)
    2.0

    >>> LA.matrix_norm(b, ord=1)
    7.0
    >>> LA.matrix_norm(b, ord=-1)
    6.0
    >>> LA.matrix_norm(b, ord=2)
    7.3484692283495345
    >>> LA.matrix_norm(b, ord=-2)
    1.8570331885190563e-016 # may vary

    """
    x = asanyarray(x)
    return norm(x, axis=(-2, -1), keepdims=keepdims, ord=ord)


def matrix_norm(x: ArrayLike, /, *, keepdims: bool = False, ord: str | int = 'fro') -> Array:
  """Compute the norm of a matrix or stack of matrices.

  JAX implementation of :func:`numpy.linalg.matrix_norm`

  Args:
    x: array of shape ``(..., M, N)`` for which to take the norm.
    keepdims: if True, keep the reduced dimensions in the output.
    ord: A string or int specifying the type of norm; default is the Frobenius norm.
      See :func:`numpy.linalg.norm` for details on available options.

  Returns:
    array containing the norm of ``x``. Has shape ``x.shape[:-2]`` if ``keepdims`` is
    False, or shape ``(..., 1, 1)`` if ``keepdims`` is True.

  See also:
    - :func:`jax.numpy.linalg.vector_norm`: Norm of a vector or stack of vectors.
    - :func:`jax.numpy.linalg.norm`: More general matrix or vector norm.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6],
    ...                [7, 8, 9]])
    >>> jnp.linalg.matrix_norm(x)
    Array(16.881943, dtype=float32)
  """
  x = ensure_arraylike('jnp.linalg.matrix_norm', x)
  return norm(x, ord=ord, keepdims=keepdims, axis=(-2, -1))

