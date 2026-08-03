from typing import Any

def transpose(array, axes=None):
    """
    Framework-agnostic version of transpose operation.
    """
    if is_numpy_array(array):
        return np.transpose(array, axes=axes)
    elif is_torch_tensor(array):
        return array.T if axes is None else array.permute(*axes)
    else:
        raise ValueError(f"Type not supported for transpose: {type(array)}.")


def transpose(self: list[int], dim0: int, dim1: int):
    ndims = len(self)
    dim0 = maybe_wrap_dim(dim0, ndims)
    dim1 = maybe_wrap_dim(dim1, ndims)
    if dim0 == dim1:
        return _copy(self)
    out: list[int] = []
    for i in range(ndims):
        if i == dim0:
            out.append(self[dim1])
        elif i == dim1:
            out.append(self[dim0])
        else:
            out.append(self[i])
    return out


def transpose(a: ArrayLike, axes=None):
    # numpy allows both .transpose(sh) and .transpose(*sh)
    # also older code uses axes being a list
    if axes in [(), None, (None,)]:
        axes = tuple(reversed(range(a.ndim)))
    elif len(axes) == 1:
        axes = axes[0]
    return a.permute(axes)


def transpose(a: TensorLikeType, dim0: int, dim1: int) -> TensorLikeType:
    _dim0, _dim1 = utils.canonicalize_dims(a.ndim, (dim0, dim1))  # type: ignore[misc]

    if a.ndim <= 1 or dim0 == dim1:
        return aten.alias.default(a)

    _permutation = list(range(a.ndim))
    _permutation[_dim0] = _dim1
    _permutation[_dim1] = _dim0
    return torch.permute(a, _permutation)


def transpose(g: jit_utils.GraphContext, self, dim0, dim1):
    if dim0 == dim1:  # micro-optimization
        return self

    # NB: Transpose in ONNX is actually a Permute
    rank = symbolic_helper._get_tensor_rank(self)
    if rank is not None:
        axes = list(range(rank))
        axes[dim0], axes[dim1] = axes[dim1], axes[dim0]
        return g.op("Transpose", self, perm_i=axes)
    else:
        raise errors.SymbolicValueError(
            "Unsupported: ONNX export of transpose for tensor of unknown rank.",
            self,
        )


def transpose(expr):
    """Matrix transpose"""
    return Transpose(expr).doit(deep=False)


def transpose(it):
    """Swap the rows and columns of the input matrix.

    >>> list(transpose([(1, 2, 3), (11, 22, 33)]))
    [(1, 11), (2, 22), (3, 33)]

    The caller should ensure that the dimensions of the input are compatible.
    If the input is empty, no output will be produced.
    """
    return _zip_strict(*it)


def transpose(a, axes):
    """Normal torch transpose is only valid for 2D matrices."""
    return a.permute(*axes)


def transpose(a):
    """
    Transpose each matrix in a stack of matrices.

    Unlike np.transpose, this only swaps the last two axes, rather than all of
    them

    Parameters
    ----------
    a : (...,M,N) array_like

    Returns
    -------
    aT : (...,N,M) ndarray
    """
    return swapaxes(a, -1, -2)


def transpose(a, axes=None):
    """
    Permute the dimensions of an array.

    This function is exactly equivalent to `numpy.transpose`.

    See Also
    --------
    numpy.transpose : Equivalent function in top-level NumPy module.

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = ma.arange(4).reshape((2,2))
    >>> x[1, 1] = ma.masked
    >>> x
    masked_array(
      data=[[0, 1],
            [2, --]],
      mask=[[False, False],
            [False,  True]],
      fill_value=999999)

    >>> ma.transpose(x)
    masked_array(
      data=[[0, 2],
            [1, --]],
      mask=[[False, False],
            [False,  True]],
      fill_value=999999)
    """
    # We can't use 'frommethod', as 'transpose' doesn't take keywords
    try:
        return a.transpose(axes)
    except AttributeError:
        return np.asarray(a).transpose(axes).view(MaskedArray)


def transpose(a, axes=None):
    """
    Returns an array with axes transposed.

    For a 1-D array, this returns an unchanged view of the original array, as a
    transposed vector is simply the same vector.
    To convert a 1-D array into a 2-D column vector, an additional dimension
    must be added, e.g., ``np.atleast_2d(a).T`` achieves this, as does
    ``a[:, np.newaxis]``.
    For a 2-D array, this is the standard matrix transpose.
    For an n-D array, if axes are given, their order indicates how the
    axes are permuted (see Examples). If axes are not provided, then
    ``transpose(a).shape == a.shape[::-1]``.

    Parameters
    ----------
    a : array_like
        Input array.
    axes : tuple or list of ints, optional
        If specified, it must be a tuple or list which contains a permutation
        of [0, 1, ..., N-1] where N is the number of axes of `a`. Negative
        indices can also be used to specify axes. The i-th axis of the returned
        array will correspond to the axis numbered ``axes[i]`` of the input.
        If not specified, defaults to ``range(a.ndim)[::-1]``, which reverses
        the order of the axes.

    Returns
    -------
    p : ndarray
        `a` with its axes permuted. A view is returned whenever possible.

    See Also
    --------
    ndarray.transpose : Equivalent method.
    moveaxis : Move axes of an array to new positions.
    argsort : Return the indices that would sort an array.

    Notes
    -----
    Use ``transpose(a, argsort(axes))`` to invert the transposition of tensors
    when using the `axes` keyword argument.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> a
    array([[1, 2],
           [3, 4]])
    >>> np.transpose(a)
    array([[1, 3],
           [2, 4]])

    >>> a = np.array([1, 2, 3, 4])
    >>> a
    array([1, 2, 3, 4])
    >>> np.transpose(a)
    array([1, 2, 3, 4])

    >>> a = np.ones((1, 2, 3))
    >>> np.transpose(a, (1, 0, 2)).shape
    (2, 1, 3)

    >>> a = np.ones((2, 3, 4, 5))
    >>> np.transpose(a).shape
    (5, 4, 3, 2)

    >>> a = np.arange(3*4*5).reshape((3, 4, 5))
    >>> np.transpose(a, (-1, 0, -2)).shape
    (5, 3, 4)

    """
    return _wrapfunc(a, 'transpose', axes)


def transpose(result: _ods_ir.Type, vector: _ods_ir.Value[_ods_ir.VectorType], permutation: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return TransposeOp(result=result, vector=vector, permutation=permutation, loc=loc, ip=ip).result


def transpose(result: _ods_ir.Type, in_: _ods_ir.Value[_ods_ir.MemRefType], permutation: _Union[_ods_ir.AffineMap, _ods_ir.AffineMapAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return TransposeOp(result=result, in_=in_, permutation=permutation, loc=loc, ip=ip).result


def transpose(operand: _ods_ir.Value[_ods_ir.RankedTensorType], permutation: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TransposeOp(operand=operand, permutation=permutation, results=results, loc=loc, ip=ip).result


def transpose(operand: _ods_ir.Value[_ods_ir.RankedTensorType], permutation: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return TransposeOp(operand=operand, permutation=permutation, results=results, loc=loc, ip=ip).result


def transpose(result: _ods_ir.Type, vector: _ods_ir.Value[_ods_ir.VectorType], permutation: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return TransposeOp(result=result, vector=vector, permutation=permutation, loc=loc, ip=ip).result


def transpose(outer_treedef: tree_util.PyTreeDef,
              inner_treedef: tree_util.PyTreeDef | None,
              pytree_to_transpose: Any) -> Any:
  """Transform a tree having tree structure (outer, inner) into one having structure (inner, outer).

  Args:
    outer_treedef: PyTreeDef representing the outer tree.
    inner_treedef: PyTreeDef representing the inner tree.
      If None, then it will be inferred from outer_treedef and the structure of
      pytree_to_transpose.
    pytree_to_transpose: the pytree to be transposed.

  Returns:
    transposed_pytree: the transposed pytree.

  Examples:
    >>> import jax
    >>> tree = [(1, 2, 3), (4, 5, 6)]
    >>> inner_structure = jax.tree.structure(('*', '*', '*'))
    >>> outer_structure = jax.tree.structure(['*', '*'])
    >>> jax.tree.transpose(outer_structure, inner_structure, tree)
    ([1, 4], [2, 5], [3, 6])

    Inferring the inner structure:

    >>> jax.tree.transpose(outer_structure, None, tree)
    ([1, 4], [2, 5], [3, 6])
  """
  return tree_util.tree_transpose(outer_treedef, inner_treedef, pytree_to_transpose)


def transpose(operand: ArrayLike,
              permutation: Sequence[int] | np.ndarray) -> Array:
  """Wraps XLA's `Transpose
  <https://www.openxla.org/xla/operation_semantics#transpose>`_
  operator.
  """
  permutation = tuple(operator.index(d) for d in permutation)
  if permutation == tuple(range(np.ndim(operand))) and isinstance(operand, Array):
    return operand
  else:
    return transpose_p.bind(operand, permutation=permutation)


def transpose(a: ArrayLike, axes: Sequence[int] | None = None) -> Array:
  """Return a transposed version of an N-dimensional array.

  JAX implementation of :func:`numpy.transpose`, implemented in terms of
  :func:`jax.lax.transpose`.

  Args:
    a: input array
    axes: optionally specify the permutation using a length-`a.ndim` sequence of integers
      ``i`` satisfying ``0 <= i < a.ndim``. Defaults to ``range(a.ndim)[::-1]``, i.e.
      reverses the order of all axes.

  Returns:
    transposed copy of the array.

  See Also:
    - :func:`jax.Array.transpose`: equivalent function via an :class:`~jax.Array` method.
    - :attr:`jax.Array.T`: equivalent function via an :class:`~jax.Array`  property.
    - :func:`jax.numpy.matrix_transpose`: transpose the last two axes of an array. This is
      suitable for working with batched 2D matrices.
    - :func:`jax.numpy.swapaxes`: swap any two axes in an array.
    - :func:`jax.numpy.moveaxis`: move an axis to another position in the array.

  Note:
    Unlike :func:`numpy.transpose`, :func:`jax.numpy.transpose` will return a copy rather
    than a view of the input array. However, under JIT, the compiler will optimize-away
    such copies when possible, so this doesn't have performance impacts in practice.

  Examples:
    For a 1D array, the transpose is the identity:

    >>> x = jnp.array([1, 2, 3, 4])
    >>> jnp.transpose(x)
    Array([1, 2, 3, 4], dtype=int32)

    For a 2D array, the transpose is a matrix transpose:

    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.transpose(x)
    Array([[1, 3],
           [2, 4]], dtype=int32)

    For an N-dimensional array, the transpose reverses the order of the axes:

    >>> x = jnp.zeros(shape=(3, 4, 5))
    >>> jnp.transpose(x).shape
    (5, 4, 3)

    The ``axes`` argument can be specified to change this default behavior:

    >>> jnp.transpose(x, (0, 2, 1)).shape
    (3, 5, 4)

    Since swapping the last two axes is a common operation, it can be done
    via its own API, :func:`jax.numpy.matrix_transpose`:

    >>> jnp.matrix_transpose(x).shape
    (3, 5, 4)

    For convenience, transposes may also be performed using the :meth:`jax.Array.transpose`
    method or the :attr:`jax.Array.T` property:

    >>> x = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> x.transpose()
    Array([[1, 3],
           [2, 4]], dtype=int32)
    >>> x.T
    Array([[1, 3],
           [2, 4]], dtype=int32)
  """
  a = util.ensure_arraylike("transpose", a)
  axes_ = list(range(a.ndim)[::-1]) if axes is None else axes
  axes_ = [_canonicalize_axis(i, np.ndim(a)) for i in axes_]
  return lax.transpose(a, axes_)

