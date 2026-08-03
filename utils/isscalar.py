from typing import Any

def isscalar(a):
    # We need to use normalize_array_like, but we don't want to export it in funcs.py
    from ._normalizations import normalize_array_like

    try:
        t = normalize_array_like(a)
        return t.numel() == 1
    except Exception:
        return False


def isscalar(var):
    return not (isarray(var) or isstring(var) or isexternal(var))


def isscalar(element):
    """
    Returns True if the type of `element` is a scalar type.

    Parameters
    ----------
    element : any
        Input argument, can be of any type and shape.

    Returns
    -------
    val : bool
        True if `element` is a scalar type, False if it is not.

    See Also
    --------
    ndim : Get the number of dimensions of an array

    Notes
    -----
    If you need a stricter way to identify a *numerical* scalar, use
    ``isinstance(x, numbers.Number)``, as that returns ``False`` for most
    non-numerical elements such as strings.

    In most cases ``np.ndim(x) == 0`` should be used instead of this function,
    as that will also return true for 0d arrays. This is how numpy overloads
    functions in the style of the ``dx`` arguments to `gradient` and
    the ``bins`` argument to `histogram`. Some key differences:

    +------------------------------------+---------------+-------------------+
    | x                                  |``isscalar(x)``|``np.ndim(x) == 0``|
    +====================================+===============+===================+
    | PEP 3141 numeric objects           | ``True``      | ``True``          |
    | (including builtins)               |               |                   |
    +------------------------------------+---------------+-------------------+
    | builtin string and buffer objects  | ``True``      | ``True``          |
    +------------------------------------+---------------+-------------------+
    | other builtin objects, like        | ``False``     | ``True``          |
    | `pathlib.Path`, `Exception`,       |               |                   |
    | the result of `re.compile`         |               |                   |
    +------------------------------------+---------------+-------------------+
    | third-party objects like           | ``False``     | ``True``          |
    | `matplotlib.figure.Figure`         |               |                   |
    +------------------------------------+---------------+-------------------+
    | zero-dimensional numpy arrays      | ``False``     | ``True``          |
    +------------------------------------+---------------+-------------------+
    | other numpy arrays                 | ``False``     | ``False``         |
    +------------------------------------+---------------+-------------------+
    | `list`, `tuple`, and other         | ``False``     | ``False``         |
    | sequence objects                   |               |                   |
    +------------------------------------+---------------+-------------------+

    Examples
    --------
    >>> import numpy as np

    >>> np.isscalar(3.1)
    True

    >>> np.isscalar(np.array(3.1))
    False

    >>> np.isscalar([3.1])
    False

    >>> np.isscalar(False)
    True

    >>> np.isscalar('numpy')
    True

    NumPy supports PEP 3141 numbers:

    >>> from fractions import Fraction
    >>> np.isscalar(Fraction(5, 17))
    True
    >>> from numbers import Number
    >>> np.isscalar(Number())
    True

    """
    return (isinstance(element, generic)
            or type(element) in ScalarType
            or isinstance(element, numbers.Number))


def isscalar(element: Any) -> bool:
  """Return True if the input is a scalar.

  JAX implementation of :func:`numpy.isscalar`. JAX's implementation differs
  from NumPy's in that it considers zero-dimensional arrays to be scalars; see
  the *Note* below for more details.

  Args:
    element: input object to check; any type is valid input.

  Returns:
    True if ``element`` is a scalar value or an array-like object with zero
    dimensions, False otherwise.

  Note:
    JAX and NumPy differ in their representation of scalar values. NumPy has
    special scalar objects (e.g. ``np.int32(0)``) which are distinct from
    zero-dimensional arrays (e.g. ``np.array(0)``), and :func:`numpy.isscalar`
    returns ``True`` for the former and ``False`` for the latter.

    JAX does not define special scalar objects, but rather represents scalars as
    zero-dimensional arrays. As such, :func:`jax.numpy.isscalar` returns ``True``
    for both scalar objects (e.g. ``0.0`` or ``np.float32(0.0)``) and array-like
    objects with zero dimensions (e.g. ``jnp.array(0.0)``, ``np.array(0.0)``).

    One reason for the different conventions in ``isscalar`` is to maintain
    JIT-invariance: i.e. the property that the result of a function should not
    change when it is JIT-compiled. Because scalar inputs are cast to
    zero-dimensional JAX arrays at JIT boundaries, the semantics of
    :func:`numpy.isscalar` are such that the result changes under JIT:

    >>> np.isscalar(1.0)
    True
    >>> jax.jit(np.isscalar)(1.0)
    Array(False, dtype=bool)

    By treating zero-dimensional arrays as scalars, :func:`jax.numpy.isscalar`
    avoids this issue:

    >>> jnp.isscalar(1.0)
    True
    >>> jax.jit(jnp.isscalar)(1.0)
    Array(True, dtype=bool)

  Examples:
    In JAX, both scalars and zero-dimensional array-like objects are considered
    scalars:

    >>> jnp.isscalar(1.0)
    True
    >>> jnp.isscalar(1 + 1j)
    True
    >>> jnp.isscalar(jnp.array(1))  # zero-dimensional JAX array
    True
    >>> jnp.isscalar(jnp.int32(1))  # JAX scalar constructor
    True
    >>> jnp.isscalar(np.array(1.0))  # zero-dimensional NumPy array
    True
    >>> jnp.isscalar(np.int32(1))  # NumPy scalar type
    True

    Arrays with one or more dimension are not considered scalars:

    >>> jnp.isscalar(jnp.array([1]))
    False
    >>> jnp.isscalar(np.array([1]))
    False

    Compare this to :func:`numpy.isscalar`, which returns ``True`` for
    scalar-typed objects, and ``False`` for *all* arrays, even those with
    zero dimensions:

    >>> np.isscalar(np.int32(1))  # scalar object
    True
    >>> np.isscalar(np.array(1))  # zero-dimensional array
    False

    In JAX, as in NumPy, objects which are not array-like are not considered
    scalars:

    >>> jnp.isscalar(None)
    False
    >>> jnp.isscalar([1])
    False
    >>> jnp.isscalar(())
    False
    >>> jnp.isscalar(slice(10))
    False
  """
  if np.isscalar(element):
    return True
  elif isinstance(element, (np.ndarray, Array)):
    return element.ndim == 0
  elif getattr(element, '__jax_array__', None) is not None:
    return asarray(element).ndim == 0
  return False

