
def identity(x: V) -> V:
    """Returns its argument. Useful for certain things in the
    environment.
    """
    return x


def identity(n, dtype=None):
    """
    Returns the square identity matrix of given size.

    Parameters
    ----------
    n : int
        Size of the returned identity matrix.
    dtype : data-type, optional
        Data-type of the output. Defaults to ``float``.

    Returns
    -------
    out : matrix
        `n` x `n` matrix with its main diagonal set to one,
        and all other elements zero.

    See Also
    --------
    numpy.identity : Equivalent array function.
    matlib.eye : More general matrix identity function.

    Examples
    --------
    >>> import numpy.matlib
    >>> np.matlib.identity(3, dtype=np.int_)
    matrix([[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]])

    """
    a = array([1] + n * [0], dtype=dtype)
    b = empty((n, n), dtype=dtype)
    b.flat = a
    return b


def identity(value):
    "Identity function."
    return value


def identity(x):
    """ Identity function. Return x

    >>> identity(3)
    3
    """
    return x


def identity(x):
    return x


def identity(x: T) -> T:
    return x


def identity(n, dtype: DTypeLike | None = None, *, like: NotImplementedType = None):
    return torch.eye(n, dtype=dtype)


def identity(a):
    return a


def identity(module, name):
    r"""Apply pruning reparameterization without pruning any units.

    Applies pruning reparameterization to the tensor corresponding to the
    parameter called ``name`` in ``module`` without actually pruning any
    units. Modifies module in place (and also return the modified module)
    by:

    1) adding a named buffer called ``name+'_mask'`` corresponding to the
       binary mask applied to the parameter ``name`` by the pruning method.
    2) replacing the parameter ``name`` by its pruned version, while the
       original (unpruned) parameter is stored in a new parameter named
       ``name+'_orig'``.

    Note:
        The mask is a tensor of ones.

    Args:
        module (nn.Module): module containing the tensor to prune.
        name (str): parameter name within ``module`` on which pruning
                will act.

    Returns:
        module (nn.Module): modified (i.e. pruned) version of the input module

    Examples:
        >>> # xdoctest: +SKIP
        >>> m = prune.identity(nn.Linear(2, 3), "bias")
        >>> print(m.bias_mask)
        tensor([1., 1., 1.])
    """
    Identity.apply(module, name)
    return module


def identity(x):
    return x


def identity(x: _T) -> _T:
    return x


def identity(x):
    yield x


def identity(x):
    return x


def identity(x):
    return x


def identity(x):
    """
    Return the argument.

    >>> o = object()
    >>> identity(o) is o
    True
    """
    return x


def identity(n, dtype='d', format=None):
    """Identity matrix in sparse format.

    Returns an identity matrix with shape ``(n, n)`` using a given
    sparse format and dtype. This differs from `eye_array` in
    that it has a square shape with ones only on the main diagonal.
    It is thus the multiplicative identity. `eye_array` allows
    rectangular shapes and the diagonal can be offset from the main one.

    .. warning::

        This function returns a sparse matrix -- not a sparse array.
        You are encouraged to use `eye_array` to take advantage
        of the sparse array functionality.

    Parameters
    ----------
    n : int
        Shape of the identity matrix.
    dtype : dtype, optional
        Data type of the matrix
    format : str, optional
        Sparse format of the result, e.g., format="csr", etc.

    Returns
    -------
    new_matrix : sparse matrix
        A square sparse matrix with ones on the main diagonal and zeros elsewhere.

    See Also
    --------
    eye_array : Sparse array of chosen shape with ones on a specified diagonal.
    eye : Sparse matrix of chosen shape with ones on a specified diagonal.

    Examples
    --------
    >>> import scipy as sp
    >>> sp.sparse.identity(3).toarray()
    array([[ 1.,  0.,  0.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.]])
    >>> sp.sparse.identity(3, dtype='int8', format='dia')
    <DIAgonal sparse matrix of dtype 'int8'
        with 3 stored elements (1 diagonals) and shape (3, 3)>
    >>> sp.sparse.eye_array(3, dtype='int8', format='dia')
    <DIAgonal sparse array of dtype 'int8'
        with 3 stored elements (1 diagonals) and shape (3, 3)>

    """
    return eye(n, n, dtype=dtype, format=format)


def identity() -> GradientTransformation:
  """Stateless identity transformation that leaves input gradients untouched.

  This function passes through the *gradient updates* unchanged.

  Note, this should not to be confused with `set_to_zero`, which maps the input
  updates to zero - which is the transform required for the *model parameters*
  to be left unchanged when the updates are applied to them.

  Returns:
    A :class:`optax.GradientTransformation` object.
  """

  def update_fn(updates, state, params=None):
    del params
    return updates, state

  return GradientTransformation(init_empty_state, update_fn)


def identity(n, dtype=None, *, like=None):
    """
    Return the identity array.

    The identity array is a square array with ones on
    the main diagonal.

    Parameters
    ----------
    n : int
        Number of rows (and columns) in `n` x `n` output.
    dtype : data-type, optional
        Data-type of the output.  Defaults to ``float``.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        `n` x `n` array with its main diagonal set to one,
        and all other elements 0.

    Examples
    --------
    >>> import numpy as np
    >>> np.identity(3)
    array([[1.,  0.,  0.],
           [0.,  1.,  0.],
           [0.,  0.,  1.]])

    """
    if like is not None:
        return _identity_with_like(like, n, dtype=dtype)

    from numpy import eye
    return eye(n, dtype=dtype, like=like)


def Identity():
  """Layer construction function for an identity layer."""
  init_fun = lambda rng, input_shape: (input_shape, ())
  apply_fun = lambda params, inputs, **kwargs: inputs
  return init_fun, apply_fun


def identity(x): return x


def identity(x): return x


def identity(x): return x


def identity(x): return x


def identity(x): return x


def identity(x: ArrayLike) -> Array:
  r"""Identity activation function.

  Returns the argument unmodified.

  Args:
    x : input array

  Returns:
    The argument `x` unmodified.

  Examples:
    >>> jax.nn.identity(jax.numpy.array([-2., -1., -0.5, 0, 0.5, 1., 2.]))
    Array([-2. , -1. , -0.5, 0. , 0.5, 1. , 2. ], dtype=float32)

  """
  return numpy_util.ensure_arraylike("identity", x)


def identity(n: DimSize, dtype: DTypeLike | None = None) -> Array:
  """Create a square identity matrix

  JAX implementation of :func:`numpy.identity`.

  Args:
    n: integer specifying the size of each array dimension.
    dtype: optional dtype; defaults to floating point.

  Returns:
    Identity array of shape ``(n, n)``.

  See also:
    :func:`jax.numpy.eye`: non-square and/or offset identity matrices.

  Examples:
    A simple 3x3 identity matrix:

    >>> jnp.identity(3)
    Array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]], dtype=float32)

    A 2x2 integer identity matrix:

    >>> jnp.identity(2, dtype=int)
    Array([[1, 0],
           [0, 1]], dtype=int32)
  """
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "identity")
  return eye(n, dtype=dtype)

