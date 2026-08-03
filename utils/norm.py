from typing import Optional

def norm(  # noqa: F811
    input,
    p: float | str | None = "fro",
    dim=None,
    keepdim=False,
    out=None,
    dtype=None,
):
    r"""Returns the matrix norm or vector norm of a given tensor.

    .. warning::

        torch.norm is deprecated and may be removed in a future PyTorch release.
        Its documentation and behavior may be incorrect, and it is no longer
        actively maintained.

        Use :func:`torch.linalg.vector_norm` when computing vector norms and
        :func:`torch.linalg.matrix_norm` when computing matrix norms.
        For a function with a similar behavior as this one see :func:`torch.linalg.norm`.
        Note, however, the signature for these functions is slightly different than the
        signature for ``torch.norm``.

    Args:
        input (Tensor): The input tensor. Its data type must be either a floating
            point or complex type. For complex inputs, the norm is calculated using the
            absolute value of each element. If the input is complex and neither
            :attr:`dtype` nor :attr:`out` is specified, the result's data type will
            be the corresponding floating point type (e.g. float if :attr:`input` is
            complexfloat).

        p (int, float, inf, -inf, 'fro', 'nuc', optional): the order of norm. Default: ``'fro'``
            The following norms can be calculated:

            ======  ==============  ==========================
            ord     matrix norm     vector norm
            ======  ==============  ==========================
            'fro'   Frobenius norm  --
            'nuc'   nuclear norm    --
            Number  --              sum(abs(x)**ord)**(1./ord)
            ======  ==============  ==========================

            The vector norm can be calculated across any number of dimensions.
            The corresponding dimensions of :attr:`input` are flattened into
            one dimension, and the norm is calculated on the flattened
            dimension.

            Frobenius norm produces the same result as ``p=2`` in all cases
            except when :attr:`dim` is a list of three or more dims, in which
            case Frobenius norm throws an error.

            Nuclear norm can only be calculated across exactly two dimensions.

        dim (int, tuple of ints, list of ints, optional):
            Specifies which dimension or dimensions of :attr:`input` to
            calculate the norm across. If :attr:`dim` is ``None``, the norm will
            be calculated across all dimensions of :attr:`input`. If the norm
            type indicated by :attr:`p` does not support the specified number of
            dimensions, an error will occur.
        keepdim (bool, optional): whether the output tensors have :attr:`dim`
            retained or not. Ignored if :attr:`dim` = ``None`` and
            :attr:`out` = ``None``. Default: ``False``
        out (Tensor, optional): the output tensor. Ignored if
            :attr:`dim` = ``None`` and :attr:`out` = ``None``.
        dtype (:class:`torch.dtype`, optional): the desired data type of
            returned tensor. If specified, the input tensor is casted to
            :attr:`dtype` while performing the operation. Default: None.

    .. note::
        Even though ``p='fro'`` supports any number of dimensions, the true
        mathematical definition of Frobenius norm only applies to tensors with
        exactly two dimensions. :func:`torch.linalg.matrix_norm` with ``ord='fro'``
        aligns with the mathematical definition, since it can only be applied across
        exactly two dimensions.

    Example::

        >>> import torch
        >>> a = torch.arange(9, dtype= torch.float) - 4
        >>> b = a.reshape((3, 3))
        >>> torch.norm(a)
        tensor(7.7460)
        >>> torch.norm(b)
        tensor(7.7460)
        >>> torch.norm(a, float('inf'))
        tensor(4.)
        >>> torch.norm(b, float('inf'))
        tensor(4.)
        >>> c = torch.tensor([[ 1, 2, 3], [-1, 1, 4]] , dtype=torch.float)
        >>> torch.norm(c, dim=0)
        tensor([1.4142, 2.2361, 5.0000])
        >>> torch.norm(c, dim=1)
        tensor([3.7417, 4.2426])
        >>> torch.norm(c, p=1, dim=1)
        tensor([6., 6.])
        >>> d = torch.arange(8, dtype=torch.float).reshape(2, 2, 2)
        >>> torch.norm(d, dim=(1, 2))
        tensor([ 3.7417, 11.2250])
        >>> torch.norm(d[0, :, :]), torch.norm(d[1, :, :])
        (tensor(3.7417), tensor(11.2250))
    """

    if has_torch_function_unary(input):
        return handle_torch_function(
            norm, (input,), input, p=p, dim=dim, keepdim=keepdim, out=out, dtype=dtype
        )

    # NB. All the repeated code and weird python is to please TorchScript.
    #     For a more compact implementation see the relevant function in `_refs/__init__.py`

    # We don't do this for MPS or sparse tensors
    if input.layout == torch.strided and input.device.type in (
        "cpu",
        "cuda",
        "xpu",
        "meta",
        torch.utils.backend_registration._privateuse1_backend_name,
    ):
        if dim is not None:
            if isinstance(dim, (int, torch.SymInt)):
                _dim = [dim]
            else:
                _dim = dim
        else:
            _dim = None  # type: ignore[assignment]

        if isinstance(p, str):
            if p == "fro" and (
                dim is None
                or isinstance(dim, (int, torch.SymInt))
                or len(dim) <= 2  # pyrefly: ignore  # bad-argument-type
            ):
                if out is None:
                    return torch.linalg.vector_norm(
                        input, 2, _dim, keepdim, dtype=dtype
                    )
                else:
                    return torch.linalg.vector_norm(
                        input, 2, _dim, keepdim, dtype=dtype, out=out
                    )

            # Here we either call the nuclear norm, or we call matrix_norm with some arguments
            # that will throw an error
            if _dim is None:
                _dim = list(range(input.ndim))
            if out is None:
                return torch.linalg.matrix_norm(input, p, _dim, keepdim, dtype=dtype)
            else:
                return torch.linalg.matrix_norm(
                    input, p, _dim, keepdim, dtype=dtype, out=out
                )
        else:
            # NB. p should be Union[str, number], not Optional!
            _p = 2.0 if p is None else p
            if out is None:
                return torch.linalg.vector_norm(input, _p, _dim, keepdim, dtype=dtype)
            else:
                return torch.linalg.vector_norm(
                    input, _p, _dim, keepdim, dtype=dtype, out=out
                )

    ndim = input.dim()

    # catch default case
    if dim is None and out is None and dtype is None and p is not None:
        if isinstance(p, str):
            if p == "fro":
                return _VF.frobenius_norm(input, dim=(), keepdim=keepdim)
        if not isinstance(p, str):
            _dim = list(range(ndim))
            return _VF.norm(input, p, dim=_dim, keepdim=keepdim)  # type: ignore[attr-defined]

    # TODO: when https://github.com/pytorch/pytorch/issues/33782 is fixed
    # remove the overloads where dim is an int and replace with BroadcastingList1
    # and remove next four lines, replace _dim with dim
    if dim is not None:
        if isinstance(dim, (int, torch.SymInt)):
            _dim = [dim]
        else:
            _dim = dim
    else:
        _dim = None  # type: ignore[assignment]

    if isinstance(p, str):
        if p == "fro":
            if dtype is not None:
                raise ValueError("dtype argument is not supported in frobenius norm")

            if _dim is None:
                _dim = list(range(ndim))
            if out is None:
                return _VF.frobenius_norm(input, _dim, keepdim=keepdim)  # type: ignore[arg-type]
            else:
                return _VF.frobenius_norm(input, _dim, keepdim=keepdim, out=out)  # type: ignore[arg-type]
        elif p == "nuc":
            if dtype is not None:
                raise ValueError("dtype argument is not supported in nuclear norm")
            if _dim is None:
                if out is None:
                    return _VF.nuclear_norm(input, keepdim=keepdim)  # type: ignore[arg-type]
                else:
                    return _VF.nuclear_norm(input, keepdim=keepdim, out=out)  # type: ignore[arg-type]
            else:
                if out is None:
                    return _VF.nuclear_norm(input, _dim, keepdim=keepdim)  # type: ignore[arg-type]
                else:
                    return _VF.nuclear_norm(input, _dim, keepdim=keepdim, out=out)  # type: ignore[arg-type]
        raise RuntimeError(f"only valid string values are 'fro' and 'nuc', found {p}")
    else:
        if _dim is None:
            _dim = list(range(ndim))

        if out is None:
            if dtype is None:
                return _VF.norm(input, p, _dim, keepdim=keepdim)  # type: ignore[attr-defined]
            else:
                return _VF.norm(input, p, _dim, keepdim=keepdim, dtype=dtype)  # type: ignore[attr-defined]
        else:
            if dtype is None:
                return _VF.norm(input, p, _dim, keepdim=keepdim, out=out)  # type: ignore[attr-defined]
            else:
                return _VF.norm(input, p, _dim, keepdim=keepdim, dtype=dtype, out=out)  # type: ignore[attr-defined]


def norm(
    input: Tensor | MaskedTensor,
    ord: float | None = 2.0,
    dim: DimOrDims = None,
    *,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}

{reduction_descr}

The identity value of norm operation, which is used to start the
reduction, is ``{identity_float32}``, except for ``ord=-inf`` it is
``{identity_ord_ninf}``.

{reduction_args}

{reduction_example}"""
    if dtype is None:
        dtype = input.dtype
    mask_input = _combine_input_and_mask(norm, input, mask, ord)
    if mask_input.layout == torch.strided:
        dim_ = _canonical_dim(dim, input.ndim)
        return torch.linalg.vector_norm(
            mask_input, ord, dim_, bool(keepdim), dtype=dtype
        )
    else:
        raise ValueError(
            f"masked norm expects strided tensor (got {mask_input.layout} tensor)"
        )


def norm(x: ArrayLike, ord=None, axis=None, keepdims: KeepDims = False):
    x = _atleast_float_1(x)
    return torch.linalg.norm(x, ord=ord, dim=axis)


def norm(
    input: TensorLikeType,
    p: float | str | None = "fro",
    dim: DimsType | None = None,
    keepdim: bool = False,
    *,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    # In these cases we compute the "Frobenius norm"
    if (
        p == "fro" and (dim is None or isinstance(dim, Dim) or len(dim) <= 2)
    ) or p is None:
        p = 2
    if isinstance(dim, Dim):
        dim = [dim]
    if isinstance(p, str):
        # Here we either call the nuclear norm, or we call matrix_norm with some arguments
        # that will throw an error
        if dim is None:
            dim = tuple(range(input.ndim))
        return torch.linalg.matrix_norm(input, p, dim, keepdim, dtype=dtype)
    else:
        return torch.linalg.vector_norm(input, p, dim, keepdim, dtype=dtype)


def norm(
    A: TensorLikeType,
    ord: float | str | None = None,
    dim: DimsType | None = None,
    keepdim: bool = False,
    *,
    dtype: torch.dtype | None = None,
) -> TensorLikeType:
    if dim is not None:
        if isinstance(dim, Dim):
            dim = (dim,)  # type: ignore[assignment]
        torch._check(
            len(dim) in (1, 2),
            lambda: f"linalg.norm: If dim is specified, it must be of length 1 or 2. Got {dim}",
        )
    elif ord is not None:
        torch._check(
            A.ndim in (1, 2),
            lambda: f"linalg.norm: If dim is not specified but ord is, the input must be 1D or 2D. Got {A.ndim}D",
        )

    if ord is not None and (
        (dim is not None and len(dim) == 2) or (dim is None and A.ndim == 2)
    ):
        if dim is None:
            dim = (0, 1)
        return matrix_norm(A, ord, dim, keepdim, dtype=dtype)
    else:
        if ord is None:
            ord = 2.0
        return vector_norm(A, ord, dim, keepdim, dtype=dtype)  # type: ignore[arg-type]


def norm(g: jit_utils.GraphContext, self, p, dim, keepdim, dtype=None):
    if p == 1:
        f = symbolic_helper._reduce_op_symbolic_helper("ReduceL1")
    elif p == 2:
        f = symbolic_helper._reduce_op_symbolic_helper("ReduceL2")
    else:
        raise errors.SymbolicValueError(
            "ONNX export only p-norms with p of 1 or 2", self
        )
    result = f(g, self, dim=dim, keepdim=keepdim)
    if dtype is not None:
        dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        result = g.op("Cast", result, to_i=_type_utils.JitScalarType(dtype).onnx_type())
    return result


def norm(point):
    """Returns the Euclidean norm of a point from origin.

    Parameters
    ==========

    point:
        This denotes a point in the dimension_al spac_e.

    Examples
    ========

    >>> from sympy.integrals.intpoly import norm
    >>> from sympy import Point
    >>> norm(Point(2, 7))
    sqrt(53)
    """
    half = S.Half
    if isinstance(point, (list, tuple)):
        return sum(coord ** 2 for coord in point) ** half
    elif isinstance(point, Point):
        if isinstance(point, Point2D):
            return (point.x ** 2 + point.y ** 2) ** half
        else:
            return (point.x ** 2 + point.y ** 2 + point.z) ** half
    elif isinstance(point, dict):
        return sum(i**2 for i in point.values()) ** half


def norm(a):
    m = mag(a)
    return (a[0] / m, a[1] / m, a[2] / m)


def norm(a, ord=None, axis=None, keepdims=False, check_finite=True):
    """
    Matrix or vector norm.

    This function is able to return one of eight different matrix norms,
    or one of an infinite number of vector norms (described below), depending
    on the value of the ``ord`` parameter. For tensors with rank different from
    1 or 2, only `ord=None` is supported.

    Parameters
    ----------
    a : array_like
        Input array. If `axis` is None, `a` must be 1-D or 2-D, unless `ord`
        is None. If both `axis` and `ord` are None, the 2-norm of
        ``a.ravel`` will be returned.
    ord : {int, inf, -inf, 'fro', 'nuc', None}, optional
        Order of the norm (see table under ``Notes``). inf means NumPy's
        `inf` object.
    axis : {int, 2-tuple of ints, None}, optional
        If `axis` is an integer, it specifies the axis of `a` along which to
        compute the vector norms. If `axis` is a 2-tuple, it specifies the
        axes that hold 2-D matrices, and the matrix norms of these matrices
        are computed. If `axis` is None then either a vector norm (when `a`
        is 1-D) or a matrix norm (when `a` is 2-D) is returned.
    keepdims : bool, optional
        If this is set to True, the axes which are normed over are left in the
        result as dimensions with size one. With this option the result will
        broadcast correctly against the original `a`.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    n : float or ndarray
        Norm of the matrix or vector(s).

    Notes
    -----
    For values of ``ord <= 0``, the result is, strictly speaking, not a
    mathematical 'norm', but it may still be useful for various numerical
    purposes.

    The following norms can be calculated:

    =====  ============================  ==========================
    ord    norm for matrices             norm for vectors
    =====  ============================  ==========================
    None   Frobenius norm                2-norm
    'fro'  Frobenius norm                --
    'nuc'  nuclear norm                  --
    inf    max(sum(abs(a), axis=1))      max(abs(a))
    -inf   min(sum(abs(a), axis=1))      min(abs(a))
    0      --                            sum(a != 0)
    1      max(sum(abs(a), axis=0))      as below
    -1     min(sum(abs(a), axis=0))      as below
    2      2-norm (largest sing. value)  as below
    -2     smallest singular value       as below
    other  --                            sum(abs(a)**ord)**(1./ord)
    =====  ============================  ==========================

    The Frobenius norm is given by [1]_:

        :math:`||A||_F = [\\sum_{i,j} abs(a_{i,j})^2]^{1/2}`

    The nuclear norm is the sum of the singular values.

    Both the Frobenius and nuclear norm orders are only defined for
    matrices.

    References
    ----------
    .. [1] G. H. Golub and C. F. Van Loan, *Matrix Computations*,
           Baltimore, MD, Johns Hopkins University Press, 1985, pg. 15

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import norm
    >>> a = np.arange(9) - 4.0
    >>> a
    array([-4., -3., -2., -1.,  0.,  1.,  2.,  3.,  4.])
    >>> b = a.reshape((3, 3))
    >>> b
    array([[-4., -3., -2.],
           [-1.,  0.,  1.],
           [ 2.,  3.,  4.]])

    >>> norm(a)
    7.745966692414834
    >>> norm(b)
    7.745966692414834
    >>> norm(b, 'fro')
    7.745966692414834
    >>> norm(a, np.inf)
    4.0
    >>> norm(b, np.inf)
    9.0
    >>> norm(a, -np.inf)
    0.0
    >>> norm(b, -np.inf)
    2.0

    >>> norm(a, 1)
    20.0
    >>> norm(b, 1)
    7.0
    >>> norm(a, -1)
    -4.6566128774142013e-010
    >>> norm(b, -1)
    6.0
    >>> norm(a, 2)
    7.745966692414834
    >>> norm(b, 2)
    7.3484692283495345

    >>> norm(a, -2)
    0.0
    >>> norm(b, -2)
    1.8570331885190563e-016
    >>> norm(a, 3)
    5.8480354764257312
    >>> norm(a, -3)
    0.0

    """
    # Differs from numpy only in non-finite handling and the use of blas.
    if check_finite:
        a = np.asarray_chkfinite(a)
    else:
        a = np.asarray(a)
    _deprecate_dtypes('norm', a)

    if a.size and a.dtype.char in 'fdFD' and axis is None and not keepdims:

        if ord in (None, 2) and (a.ndim == 1):
            # use blas for fast and stable euclidean norm
            nrm2 = get_blas_funcs('nrm2', dtype=a.dtype, ilp64='preferred')
            return nrm2(a)

        if a.ndim == 2:
            # Use lapack for a couple fast matrix norms.
            # For some reason the *lange frobenius norm is slow.
            lange_args = None
            # Make sure this works if the user uses the axis keywords
            # to apply the norm to the transpose.
            if ord == 1:
                if np.isfortran(a):
                    lange_args = '1', a
                elif np.isfortran(a.T):
                    lange_args = 'i', a.T
            elif ord == np.inf:
                if np.isfortran(a):
                    lange_args = 'i', a
                elif np.isfortran(a.T):
                    lange_args = '1', a.T
            if lange_args:
                lange = get_lapack_funcs('lange', dtype=a.dtype, ilp64='preferred')
                return lange(*lange_args)

    # fall back to numpy in every other case
    return np.linalg.norm(a, ord=ord, axis=axis, keepdims=keepdims)


def norm(x):
    if not USE_NAIVE_MATH:
        return np.linalg.norm(x)
    # NOTE: Avoid np.pow! And exponentiation in general!
    # It appears that in Fortran, x*x and x**2 are the same, but in Python they are not!
    # Try it with x = 5 - 1e-15
    result = np.sqrt(sum([xi*xi for xi in x]))
    return result


def norm(x, ord=None, axis=None):
    """
    Norm of a sparse matrix.

    This function is able to return one of seven different matrix norms,
    depending on the value of the ``ord`` parameter.

    Parameters
    ----------
    x : a sparse array
        Input sparse array.
    ord : {non-zero int, inf, -inf, 'fro'}, optional
        Order of the norm (see table under ``Notes``). inf means numpy's
        `inf` object.
    axis : {int, 2-tuple of ints, None}, optional
        If `axis` is an integer, it specifies the axis of `x` along which to
        compute the vector norms.  If `axis` is a 2-tuple, it specifies the
        axes that hold 2-D matrices, and the matrix norms of these matrices
        are computed.  If `axis` is None then either a vector norm (when `x`
        is 1-D) or a matrix norm (when `x` is 2-D) is returned.

    Returns
    -------
    n : float or ndarray
        The selected norm of `x`.

    Notes
    -----
    Some of the ord are not implemented because some associated functions like,
    _multi_svd_norm, are not yet available for sparse array.

    This docstring is modified based on numpy.linalg.norm.
    https://github.com/numpy/numpy/blob/main/numpy/linalg/linalg.py

    The following norms can be calculated:

    =====  ============================
    ord    norm for sparse arrays
    =====  ============================
    None   Frobenius norm
    'fro'  Frobenius norm
    inf    max(sum(abs(x), axis=1))
    -inf   min(sum(abs(x), axis=1))
    0      abs(x).sum(axis=axis)
    1      max(sum(abs(x), axis=0))
    -1     min(sum(abs(x), axis=0))
    2      Spectral norm (the largest singular value)
    -2     Not implemented
    other  Not implemented
    =====  ============================

    The Frobenius norm is given by [1]_:

    :math:`||A||_F = [\\sum_{i,j} abs(a_{i,j})^2]^{1/2}`

    References
    ----------
    .. [1] G. H. Golub and C. F. Van Loan, *Matrix Computations*,
        Baltimore, MD, Johns Hopkins University Press, 1985, pg. 15

    Examples
    --------
    >>> from scipy.sparse import csr_array, diags_array
    >>> import numpy as np
    >>> from scipy.sparse.linalg import norm
    >>> a = np.arange(9) - 4
    >>> a
    array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    >>> b = a.reshape((3, 3))
    >>> b
    array([[-4, -3, -2],
           [-1, 0, 1],
           [ 2, 3, 4]])

    >>> b = csr_array(b)
    >>> norm(b)
    7.745966692414834
    >>> norm(b, 'fro')
    7.745966692414834
    >>> norm(b, np.inf)
    9
    >>> norm(b, -np.inf)
    2
    >>> norm(b, 1)
    7
    >>> norm(b, -1)
    6

    The matrix 2-norm or the spectral norm is the largest singular
    value, computed approximately and with limitations.

    >>> b = diags_array([-1, 1], offsets=[0, 1], shape=(9, 10))
    >>> norm(b, 2)
    1.9753...
    """
    x = convert_pydata_sparse_to_scipy(x, target_format="csr")
    if not issparse(x):
        raise TypeError("input is not sparse. use numpy.linalg.norm")

    # Check the default case first and handle it immediately.
    if axis is None and ord in (None, 'fro', 'f'):
        return _sparse_frobenius_norm(x)

    # DIA format doesn't support .max() or .min() methods.
    if x.format == 'dia':
        x = x.tocsr()

    if axis is None:
        axis = tuple(range(x.ndim))
    elif not isinstance(axis, tuple):
        msg = "'axis' must be None, an integer or a tuple of integers"
        try:
            int_axis = int(axis)
        except TypeError as e:
            raise TypeError(msg) from e
        if axis != int_axis:
            raise TypeError(msg)
        axis = (int_axis,)

    nd = x.ndim
    if len(axis) == 2:
        row_axis, col_axis = axis
        if not (-nd <= row_axis < nd and -nd <= col_axis < nd):
            message = f'Invalid axis {axis!r} for an array with shape {x.shape!r}'
            raise ValueError(message)
        if row_axis % nd == col_axis % nd:
            raise ValueError('Duplicate axes given.')
        if ord == 2:
            _, s, _ = svds(x, k=1, solver="arpack", rng=None)
            return s[0]
        if ord == -2:
            raise NotImplementedError
            #return _multi_svd_norm(x, row_axis, col_axis, amin)
        if ord in (None, 'f', 'fro'):
            # The axis order does not matter for this norm.
            return _sparse_frobenius_norm(x)
        if np.can_cast(x.dtype, float):
            x = x.astype(float, copy=False)
        if ord == 1:
            return abs(x).sum(axis=row_axis).max()
        elif ord == np.inf:
            return abs(x).sum(axis=col_axis).max()
        elif ord == -1:
            return abs(x).sum(axis=row_axis).min()
        elif ord == -np.inf:
            return abs(x).sum(axis=col_axis).min()
        else:
            raise ValueError("Invalid norm order for matrices.")
    elif len(axis) == 1:
        a, = axis
        if not (-nd <= a < nd):
            message = f'Invalid axis {axis!r} for an array with shape {x.shape!r}'
            raise ValueError(message)
        if ord == 0:
            return x.count_nonzero(axis=a)
        if np.can_cast(x.dtype, float):
            x = x.astype(float, copy=False)
        if ord == np.inf:
            return _ravel(abs(x).max(axis=a))
        if ord == -np.inf:
            return _ravel(abs(x).min(axis=a))
        if ord == 1:
            # special case for speedup
            return _ravel(abs(x).sum(axis=a))
        if ord in (2, None):
            return _ravel(sqrt(abs(x).power(2).sum(axis=a)))
        try:
            ord + 1
        except TypeError as e:
            raise ValueError('Invalid norm order for vectors.') from e
        return np.power(abs(x).power(ord).sum(axis=a), 1 / ord)
    else:
        raise ValueError("Improper number of dimensions to norm.")


def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size ** 0.5


def norm(x, ord=None, axis=None, keepdims=False):
    """
    Matrix or vector norm.

    This function is able to return one of eight different matrix norms,
    or one of an infinite number of vector norms (described below), depending
    on the value of the ``ord`` parameter.

    Parameters
    ----------
    x : array_like
        Input array.  If `axis` is None, `x` must be 1-D or 2-D, unless `ord`
        is None. If both `axis` and `ord` are None, the 2-norm of
        ``x.ravel`` will be returned.
    ord : {int, float, inf, -inf, 'fro', 'nuc'}, optional
        Order of the norm (see table under ``Notes`` for what values are
        supported for matrices and vectors respectively). inf means numpy's
        `inf` object. The default is None.
    axis : {None, int, 2-tuple of ints}, optional.
        If `axis` is an integer, it specifies the axis of `x` along which to
        compute the vector norms.  If `axis` is a 2-tuple, it specifies the
        axes that hold 2-D matrices, and the matrix norms of these matrices
        are computed.  If `axis` is None then either a vector norm (when `x`
        is 1-D) or a matrix norm (when `x` is 2-D) is returned. The default
        is None.

    keepdims : bool, optional
        If this is set to True, the axes which are normed over are left in the
        result as dimensions with size one.  With this option the result will
        broadcast correctly against the original `x`.

    Returns
    -------
    n : float or ndarray
        Norm of the matrix or vector(s).

    See Also
    --------
    scipy.linalg.norm : Similar function in SciPy.

    Notes
    -----
    For values of ``ord < 1``, the result is, strictly speaking, not a
    mathematical 'norm', but it may still be useful for various numerical
    purposes.

    The following norms can be calculated:

    =====  ============================  ==========================
    ord    norm for matrices             norm for vectors
    =====  ============================  ==========================
    None   Frobenius norm                2-norm
    'fro'  Frobenius norm                --
    'nuc'  nuclear norm                  --
    inf    max(sum(abs(x), axis=1))      max(abs(x))
    -inf   min(sum(abs(x), axis=1))      min(abs(x))
    0      --                            sum(x != 0)
    1      max(sum(abs(x), axis=0))      as below
    -1     min(sum(abs(x), axis=0))      as below
    2      2-norm (largest sing. value)  as below
    -2     smallest singular value       as below
    other  --                            sum(abs(x)**ord)**(1./ord)
    =====  ============================  ==========================

    The Frobenius norm is given by [1]_:

    :math:`||A||_F = [\\sum_{i,j} abs(a_{i,j})^2]^{1/2}`

    The nuclear norm is the sum of the singular values.

    Both the Frobenius and nuclear norm orders are only defined for
    matrices and raise a ValueError when ``x.ndim != 2``.

    References
    ----------
    .. [1] G. H. Golub and C. F. Van Loan, *Matrix Computations*,
           Baltimore, MD, Johns Hopkins University Press, 1985, pg. 15

    Examples
    --------

    >>> import numpy as np
    >>> from numpy import linalg as LA
    >>> a = np.arange(9) - 4
    >>> a
    array([-4, -3, -2, ...,  2,  3,  4])
    >>> b = a.reshape((3, 3))
    >>> b
    array([[-4, -3, -2],
           [-1,  0,  1],
           [ 2,  3,  4]])

    >>> LA.norm(a)
    7.745966692414834
    >>> LA.norm(b)
    7.745966692414834
    >>> LA.norm(b, 'fro')
    7.745966692414834
    >>> LA.norm(a, np.inf)
    4.0
    >>> LA.norm(b, np.inf)
    9.0
    >>> LA.norm(a, -np.inf)
    0.0
    >>> LA.norm(b, -np.inf)
    2.0

    >>> LA.norm(a, 1)
    20.0
    >>> LA.norm(b, 1)
    7.0
    >>> LA.norm(a, -1)
    -4.6566128774142013e-010
    >>> LA.norm(b, -1)
    6.0
    >>> LA.norm(a, 2)
    7.745966692414834
    >>> LA.norm(b, 2)
    7.3484692283495345

    >>> LA.norm(a, -2)
    0.0
    >>> LA.norm(b, -2)
    1.8570331885190563e-016 # may vary
    >>> LA.norm(a, 3)
    5.8480354764257312 # may vary
    >>> LA.norm(a, -3)
    0.0

    Using the `axis` argument to compute vector norms:

    >>> c = np.array([[ 1, 2, 3],
    ...               [-1, 1, 4]])
    >>> LA.norm(c, axis=0)
    array([ 1.41421356,  2.23606798,  5.        ])
    >>> LA.norm(c, axis=1)
    array([ 3.74165739,  4.24264069])
    >>> LA.norm(c, ord=1, axis=1)
    array([ 6.,  6.])

    Using the `axis` argument to compute matrix norms:

    >>> m = np.arange(8).reshape(2,2,2)
    >>> LA.norm(m, axis=(1,2))
    array([  3.74165739,  11.22497216])
    >>> LA.norm(m[0, :, :]), LA.norm(m[1, :, :])
    (3.7416573867739413, 11.224972160321824)

    """
    x = asarray(x)

    if not issubclass(x.dtype.type, (inexact, object_)):
        x = x.astype(float)

    # Immediately handle some default, simple, fast, and common cases.
    if axis is None:
        ndim = x.ndim
        if (
            (ord is None) or
            (ord in ('f', 'fro') and ndim == 2) or
            (ord == 2 and ndim == 1)
        ):
            x = x.ravel(order='K')
            if isComplexType(x.dtype.type):
                x_real = x.real
                x_imag = x.imag
                sqnorm = x_real.dot(x_real) + x_imag.dot(x_imag)
            else:
                sqnorm = x.dot(x)
            ret = sqrt(sqnorm)
            if keepdims:
                ret = ret.reshape(ndim * [1])
            return ret

    # Normalize the `axis` argument to a tuple.
    nd = x.ndim
    if axis is None:
        axis = tuple(range(nd))
    elif not isinstance(axis, tuple):
        try:
            axis = int(axis)
        except Exception as e:
            raise TypeError(
                "'axis' must be None, an integer or a tuple of integers"
            ) from e
        axis = (axis,)

    if len(axis) == 1:
        if ord == inf:
            return abs(x).max(axis=axis, keepdims=keepdims, initial=0)
        elif ord == -inf:
            return abs(x).min(axis=axis, keepdims=keepdims)
        elif ord == 0:
            # Zero norm
            return (
                (x != 0)
                .astype(x.real.dtype)
                .sum(axis=axis, keepdims=keepdims)
            )
        elif ord == 1:
            # special case for speedup
            return add.reduce(abs(x), axis=axis, keepdims=keepdims)
        elif ord is None or ord == 2:
            # special case for speedup
            s = (x.conj() * x).real
            return sqrt(add.reduce(s, axis=axis, keepdims=keepdims))
        # None of the str-type keywords for ord ('fro', 'nuc')
        # are valid for vectors
        elif isinstance(ord, str):
            raise ValueError(f"Invalid norm order '{ord}' for vectors")
        else:
            absx = abs(x)
            absx **= ord
            ret = add.reduce(absx, axis=axis, keepdims=keepdims)
            ret **= reciprocal(ord, dtype=ret.dtype)
            return ret
    elif len(axis) == 2:
        row_axis, col_axis = axis
        row_axis = normalize_axis_index(row_axis, nd)
        col_axis = normalize_axis_index(col_axis, nd)
        if row_axis == col_axis:
            raise ValueError('Duplicate axes given.')
        if ord == 2:
            ret = _multi_svd_norm(x, row_axis, col_axis, amax, 0)
        elif ord == -2:
            ret = _multi_svd_norm(x, row_axis, col_axis, amin)
        elif ord == 1:
            if col_axis > row_axis:
                col_axis -= 1
            ret = add.reduce(abs(x), axis=row_axis).max(axis=col_axis, initial=0)
        elif ord == inf:
            if row_axis > col_axis:
                row_axis -= 1
            ret = add.reduce(abs(x), axis=col_axis).max(axis=row_axis, initial=0)
        elif ord == -1:
            if col_axis > row_axis:
                col_axis -= 1
            ret = add.reduce(abs(x), axis=row_axis).min(axis=col_axis)
        elif ord == -inf:
            if row_axis > col_axis:
                row_axis -= 1
            ret = add.reduce(abs(x), axis=col_axis).min(axis=row_axis)
        elif ord in [None, 'fro', 'f']:
            ret = sqrt(add.reduce((x.conj() * x).real, axis=axis))
        elif ord == 'nuc':
            ret = _multi_svd_norm(x, row_axis, col_axis, sum, 0)
        else:
            raise ValueError("Invalid norm order for matrices.")
        if keepdims:
            ret_shape = list(x.shape)
            ret_shape[axis[0]] = 1
            ret_shape[axis[1]] = 1
            ret = ret.reshape(ret_shape)
        return ret
    else:
        raise ValueError("Improper number of dimensions to norm.")


def norm(x: ArrayLike, ord: int | str | None = None,
         axis: None | tuple[int, ...] | int = None,
         keepdims: bool = False) -> Array:
  """Compute the norm of a matrix or vector.

  JAX implementation of :func:`numpy.linalg.norm`.

  Args:
    x: N-dimensional array for which the norm will be computed.
    ord: specify the kind of norm to take. Default is Frobenius norm for matrices,
      and the 2-norm for vectors. For other options, see Notes below.
    axis: integer or sequence of integers specifying the axes over which the norm
      will be computed. For a single axis, compute a vector norm. For two axes,
      compute a matrix norm. Defaults to all axes of ``x``.
    keepdims: if True, the output array will have the same number of dimensions as
      the input, with the size of reduced axes replaced by ``1`` (default: False).

  Returns:
    array containing the specified norm of x.

  Notes:
    The flavor of norm computed depends on the value of ``ord`` and the number of
    axes being reduced.

    For **vector norms** (i.e. a single axis reduction):

    - ``ord=None`` (default) computes the 2-norm
    - ``ord=inf`` computes ``max(abs(x))``
    - ``ord=-inf`` computes min(abs(x))``
    - ``ord=0`` computes ``sum(x!=0)``
    - for other numerical values, computes ``sum(abs(x) ** ord)**(1/ord)``

    For **matrix norms** (i.e. two axes reductions):

    - ``ord='fro'`` or ``ord=None`` (default) computes the Frobenius norm
    - ``ord='nuc'`` computes the nuclear norm, or the sum of the singular values
    - ``ord=1`` computes ``max(abs(x).sum(0))``
    - ``ord=-1`` computes ``min(abs(x).sum(0))``
    - ``ord=2`` computes the 2-norm, i.e. the largest singular value
    - ``ord=-2`` computes the smallest singular value

    In the special case of ``ord=None`` and ``axis=None``, this function accepts an
    array of any dimension and computes the vector 2-norm of the flattened array.

  Examples:
    Vector norms:

    >>> x = jnp.array([3., 4., 12.])
    >>> jnp.linalg.norm(x)
    Array(13., dtype=float32)
    >>> jnp.linalg.norm(x, ord=1)
    Array(19., dtype=float32)
    >>> jnp.linalg.norm(x, ord=0)
    Array(3., dtype=float32)

    Matrix norms:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [4., 5., 7.]])
    >>> jnp.linalg.norm(x)  # Frobenius norm
    Array(10.198039, dtype=float32)
    >>> jnp.linalg.norm(x, ord='nuc')  # nuclear norm
    Array(10.762535, dtype=float32)
    >>> jnp.linalg.norm(x, ord=1)  # 1-norm
    Array(10., dtype=float32)

    Batched vector norm:

    >>> jnp.linalg.norm(x, axis=1)
    Array([3.7416575, 9.486833 ], dtype=float32)
  """
  x = ensure_arraylike("jnp.linalg.norm", x)
  x, = promote_dtypes_inexact(x)
  x_shape = np.shape(x)
  ndim = len(x_shape)

  if axis is None:
    # NumPy has an undocumented behavior that admits arbitrary rank inputs if
    # `ord` is None: https://github.com/numpy/numpy/issues/14215
    if ord is None:
      return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), keepdims=keepdims))
    axis = tuple(range(ndim))
  elif isinstance(axis, tuple):
    axis = tuple(canonicalize_axis(x, ndim) for x in axis)
  else:
    axis = (canonicalize_axis(axis, ndim),)

  match axis:
    case [_]:
      return vector_norm(x, ord=2 if ord is None else ord, axis=axis, keepdims=keepdims)
    case [row_axis, col_axis]:
      if ord is None or ord in ('f', 'fro'):
        return ufuncs.sqrt(reductions.sum(ufuncs.real(x * ufuncs.conj(x)), axis=axis,
                                        keepdims=keepdims))
      elif ord == 1:
        if not keepdims and col_axis > row_axis:
          col_axis -= 1
        return reductions.amax(reductions.sum(ufuncs.abs(x), axis=row_axis, keepdims=keepdims),
                              axis=col_axis, keepdims=keepdims, initial=0)
      elif ord == -1:
        if not keepdims and col_axis > row_axis:
          col_axis -= 1
        return reductions.amin(reductions.sum(ufuncs.abs(x), axis=row_axis, keepdims=keepdims),
                              axis=col_axis, keepdims=keepdims)
      elif ord == np.inf:
        if not keepdims and row_axis > col_axis:
          row_axis -= 1
        return reductions.amax(reductions.sum(ufuncs.abs(x), axis=col_axis, keepdims=keepdims),
                      axis=row_axis, keepdims=keepdims, initial=0)
      elif ord == -np.inf:
        if not keepdims and row_axis > col_axis:
          row_axis -= 1
        return reductions.amin(reductions.sum(ufuncs.abs(x), axis=col_axis, keepdims=keepdims),
                      axis=row_axis, keepdims=keepdims)
      elif ord in ('nuc', 2, -2):
        x = jnp.moveaxis(x, axis, (-2, -1))
        s = svd(x, compute_uv=False)
        if ord == 2:
          y = reductions.amax(s, axis=-1, initial=0)
        elif ord == -2:
          y = reductions.amin(s, axis=-1)
        else:
          y = reductions.sum(s, axis=-1)
        if keepdims:
          y = jnp.expand_dims(y, axis)
        return y
      else:
        raise ValueError(f"Invalid order '{ord}' for matrix norm.")
    case _:
      raise ValueError(f"Improper number of axes for norm: {axis=}. Pass one axis to"
                       " compute a vector-norm, or two axes to compute a matrix-norm.")


def norm(
    x: FloatArray['*d'],
    axis: Optional[int] = None,
    keepdims: bool = False,
) -> FloatArray['*d']:
  """Like `np.linalg.norm` but auto-support jnp, tnp, np."""
  if lazy.is_tf(x):  # TODO(b/219427516): tnp.linalg.norm missing
    return lazy.tf.norm(x, axis=axis, keepdims=keepdims)
  xnp = lazy.get_xnp(x)
  return xnp.linalg.norm(x, axis=axis, keepdims=keepdims)

