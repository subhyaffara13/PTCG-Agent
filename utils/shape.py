
def shape(a: ArrayLike):
    return tuple(a.shape)


def shape(source, kind=None):
    """ Creates an AST node for a function call to Fortran's "shape(...)"

    Parameters
    ==========

    source : Symbol or String
    kind : expr

    Examples
    ========

    >>> from sympy import fcode
    >>> from sympy.codegen.fnodes import shape
    >>> shp = shape('x')
    >>> fcode(shp, source_format='free')
    'shape(x)'

    """
    return FunctionCall(
        'shape',
        [_printable(source)] +
        ([_printable(kind)] if kind else [])
    )


def shape(expr):
    """
    Return the shape of the *expr* as a tuple. *expr* should represent
    suitable object such as matrix or array.

    Parameters
    ==========

    expr : SymPy object having ``MatrixKind`` or ``ArrayKind``.

    Raises
    ======

    NoShapeError : Raised when object with wrong kind is passed.

    Examples
    ========

    This function returns the shape of any object representing matrix or array.

    >>> from sympy import shape, Array, ImmutableDenseMatrix, Integral
    >>> from sympy.abc import x
    >>> A = Array([1, 2])
    >>> shape(A)
    (2,)
    >>> shape(Integral(A, x))
    (2,)
    >>> M = ImmutableDenseMatrix([1, 2])
    >>> shape(M)
    (2, 1)
    >>> shape(Integral(M, x))
    (2, 1)

    You can support new type by dispatching.

    >>> from sympy import Expr
    >>> class NewExpr(Expr):
    ...     pass
    >>> @shape.register(NewExpr)
    ... def _(expr):
    ...     return shape(expr.args[0])
    >>> shape(NewExpr(M))
    (2, 1)

    If unsuitable expression is passed, ``NoShapeError()`` will be raised.

    >>> shape(Integral(x, x))
    Traceback (most recent call last):
      ...
    sympy.tensor.functions.NoShapeError: shape() called on non-array object: Integral(x, x)

    Notes
    =====

    Array-like classes (such as ``Matrix`` or ``NDimArray``) has ``shape``
    property which returns its shape, but it cannot be used for non-array
    classes containing array. This function returns the shape of any
    registered object representing array.

    """
    if hasattr(expr, "shape"):
        return expr.shape
    raise NoShapeError(
        "%s does not have shape, or its type is not registered to shape()." % expr)


def shape(obj):
    "maskedarray version of the numpy function."
    return np.shape(getdata(obj))


def shape(a):
    """
    Return the shape of an array.

    Parameters
    ----------
    a : array_like
        Input array.

    Returns
    -------
    shape : tuple of ints
        The elements of the shape tuple give the lengths of the
        corresponding array dimensions.

    See Also
    --------
    len : ``len(a)`` is equivalent to ``np.shape(a)[0]`` for N-D arrays with
          ``N>=1``.
    ndarray.shape : Equivalent array method.

    Examples
    --------
    >>> import numpy as np
    >>> np.shape(np.eye(3))
    (3, 3)
    >>> np.shape([[1, 3]])
    (1, 2)
    >>> np.shape([0])
    (1,)
    >>> np.shape(0)
    ()

    >>> a = np.array([(1, 2), (3, 4), (5, 6)],
    ...              dtype=[('x', 'i4'), ('y', 'i4')])
    >>> np.shape(a)
    (3,)
    >>> a.shape
    (3,)

    """
    try:
        result = a.shape
    except AttributeError:
        result = asarray(a).shape
    return result


def shape(a: ArrayLike | SupportsShape) -> tuple[int, ...]:
  """Return the shape an array.

  JAX implementation of :func:`numpy.shape`. Unlike ``np.shape``, this function
  raises a :class:`TypeError` if the input is a collection such as a list or
  tuple.

  Args:
    a: array-like object, or any object with a ``shape`` attribute.

  Returns:
    An tuple of integers representing the shape of ``a``.

  Examples:
    Shape for arrays:

    >>> x = jnp.arange(10)
    >>> jnp.shape(x)
    (10,)
    >>> y = jnp.ones((2, 3))
    >>> jnp.shape(y)
    (2, 3)

    This also works for scalars:

    >>> jnp.shape(3.14)
    ()

    For arrays, this can also be accessed via the :attr:`jax.Array.shape` property:

    >>> x.shape
    (10,)
  """
  if hasattr(a, "shape"):
    return a.shape
  # Deprecation warning added 2025-2-20.
  check_arraylike("shape", a, emit_warning=True)
  m = getattr(a, "__jax_array__", None)
  if m is not None:
    a = m()
  # NumPy dispatches to a.shape if available.
  return np.shape(a)

