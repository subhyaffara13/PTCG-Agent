import math


def size(a: ArrayLike, axis=None):
    if axis is None:
        return a.numel()
    else:
        return a.shape[axis]


def size(g: jit_utils.GraphContext, self, dim=None):
    if dim is None:
        return g.op("Shape", self)
    return symbolic_helper._size_helper(g, self, dim)


def size(g: jit_utils.GraphContext, self, dim=None):
    if dim is None:
        return g.op("Shape", self)
    if symbolic_helper._maybe_get_const(dim, "i") < 0:
        rank = symbolic_helper._get_tensor_rank(self)
        if rank is not None:
            dim = symbolic_helper._maybe_get_const(dim, "i") + rank
            dim = g.op("Constant", value_t=torch.tensor(dim))
    return symbolic_helper._size_helper(g, self, dim)


def size(layout: LayoutOrIntTuple) -> int:
    if is_layout(layout):
        return layout.size()
    return product(layout)


def size(array, dim=None, kind=None):
    """ Creates an AST node for a function call to Fortran's "size(...)"

    Examples
    ========

    >>> from sympy import fcode, Symbol
    >>> from sympy.codegen.ast import FunctionDefinition, real, Return
    >>> from sympy.codegen.fnodes import array, sum_, size
    >>> a = Symbol('a', real=True)
    >>> body = [Return((sum_(a**2)/size(a))**.5)]
    >>> arr = array(a, dim=[':'], intent='in')
    >>> fd = FunctionDefinition(real, 'rms', [arr], body)
    >>> print(fcode(fd, source_format='free', standard=2003))
    real*8 function rms(a)
    real*8, dimension(:), intent(in) :: a
    rms = sqrt(sum(a**2)*1d0/size(a))
    end function

    """
    return FunctionCall(
        'size',
        [_printable(array)] +
        ([_printable(dim)] if dim else []) +
        ([_printable(kind)] if kind else [])
    )


def size(x: HasShape[Collection[SupportsIndex]]) -> int: ...


def size(x: HasShape[Collection[SupportsIndex | None]]) -> int | None: ...


def size(x: HasShape[Collection[SupportsIndex | None]]) -> int | None:
    """
    Return the total number of elements of x.

    This is equivalent to `x.size` according to the `standard
    <https://data-apis.org/array-api/latest/API_specification/generated/array_api.array.size.html>`__.

    This helper is included because PyTorch defines `size` in an
    :external+torch:meth:`incompatible way <torch.Tensor.size>`.
    It also fixes dask.array's behaviour which returns nan for unknown sizes, whereas
    the standard requires None.
    """
    # Lazy API compliant arrays, such as ndonnx, can contain None in their shape
    if None in x.shape:
        return None
    out = math.prod(cast("Collection[SupportsIndex]", x.shape))
    # dask.array.Array.shape can contain NaN
    return None if math.isnan(out) else out


def size(obj, axis=None):
    "maskedarray version of the numpy function."
    return np.size(getdata(obj), axis)


def size(a, axis=None):
    """
    Return the number of elements along a given axis.

    Parameters
    ----------
    a : array_like
        Input data.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the elements are counted.  By default, give
        the total number of elements.

        .. versionchanged:: 2.4
           Extended to accept multiple axes.

    Returns
    -------
    element_count : int
        Number of elements along the specified axis.

    See Also
    --------
    shape : dimensions of array
    ndarray.shape : dimensions of array
    ndarray.size : number of elements in array

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1,2,3],[4,5,6]])
    >>> np.size(a)
    6
    >>> np.size(a,axis=1)
    3
    >>> np.size(a,axis=0)
    2
    >>> np.size(a,axis=(0,1))
    6

    """
    if axis is None:
        try:
            return a.size
        except AttributeError:
            return asarray(a).size
    else:
        _shape = shape(a)
        from .numeric import normalize_axis_tuple
        axis = normalize_axis_tuple(axis, len(_shape), allow_duplicate=False)
        return math.prod(_shape[ax] for ax in axis)


def size(a: ArrayLike | SupportsSize | SupportsShape, axis: int | Sequence[int] | None = None) -> int:
  """Return number of elements along a given axis.

  JAX implementation of :func:`numpy.size`. Unlike ``np.size``, this function
  raises a :class:`TypeError` if the input is a collection such as a list or
  tuple.

  Args:
    a: array-like object, or any object with a ``size`` attribute when ``axis`` is not
      specified, or with a ``shape`` attribute when ``axis`` is specified.
    axis: optional integer or sequence of integers indicating which axis or axes to count
      elements along. ``None`` (the default) returns the total number of elements.

  Returns:
    An integer specifying the number of elements in ``a``.

  Examples:
    Size for arrays:

    >>> x = jnp.arange(10)
    >>> jnp.size(x)
    10
    >>> y = jnp.ones((2, 3))
    >>> jnp.size(y)
    6
    >>> jnp.size(y, axis=1)
    3
    >>> jnp.size(y, axis=(1,))
    3
    >>> jnp.size(y, axis=(0, 1))
    6

    This also works for scalars:

    >>> jnp.size(3.14)
    1

    For arrays, this can also be accessed via the :attr:`jax.Array.size` property:

    >>> y.size
    6
  """
  check_arraylike("size", a, emit_warning=True)
  if axis is None and hasattr(a, "size"):
    return a.size
  _shape = shape(a)  # pyrefly: ignore[bad-argument-type]
  axis = canonicalize_axis_tuple(axis, len(_shape), allow_duplicate=False)
  return math.prod(_shape[i] for i in axis)

