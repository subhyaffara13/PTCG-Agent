
def extract(iterable, indices):
    """Yield values at the specified indices.

    Example:

        >>> data = 'abcdefghijklmnopqrstuvwxyz'
        >>> list(extract(data, [7, 4, 11, 11, 14]))
        ['h', 'e', 'l', 'l', 'o']

    The *iterable* is consumed lazily and can be infinite.
    The *indices* are consumed immediately and must be finite.

    Raises ``IndexError`` if an index lies beyond the iterable.
    Raises ``ValueError`` for negative indices.
    """

    iterator = iter(iterable)
    index_and_position = sorted(zip(indices, count()))

    if index_and_position and index_and_position[0][0] < 0:
        raise ValueError('Indices must be non-negative')

    buffer = {}
    iterator_position = -1
    next_to_emit = 0

    for index, order in index_and_position:
        advance = index - iterator_position
        if advance:
            try:
                value = next(islice(iterator, advance - 1, None))
            except StopIteration:
                raise IndexError(index)
            iterator_position = index

        buffer[order] = value

        while next_to_emit in buffer:
            yield buffer.pop(next_to_emit)
            next_to_emit += 1


def extract(model: onnx.ModelProto):
    idx = _find_tuning_results_in_props(model.metadata_props)
    if idx < 0:
        return None

    tuning_results_prop = model.metadata_props[idx]
    return json.loads(tuning_results_prop.value)


def extract(condition, arr):
    """
    Return the elements of an array that satisfy some condition.

    This is equivalent to ``np.compress(ravel(condition), ravel(arr))``.  If
    `condition` is boolean ``np.extract`` is equivalent to ``arr[condition]``.

    Note that `place` does the exact opposite of `extract`.

    Parameters
    ----------
    condition : array_like
        An array whose nonzero or True entries indicate the elements of `arr`
        to extract.
    arr : array_like
        Input array of the same size as `condition`.

    Returns
    -------
    extract : ndarray
        Rank 1 array of values from `arr` where `condition` is True.

    See Also
    --------
    take, put, copyto, compress, place

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(12).reshape((3, 4))
    >>> arr
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]])
    >>> condition = np.mod(arr, 3)==0
    >>> condition
    array([[ True, False, False,  True],
           [False, False,  True, False],
           [False,  True, False, False]])
    >>> np.extract(condition, arr)
    array([0, 3, 6, 9])


    If `condition` is boolean:

    >>> arr[condition]
    array([0, 3, 6, 9])

    """
    return _nx.take(ravel(arr), nonzero(ravel(condition))[0])


def extract(source: _ods_ir.Value[_ods_ir.VectorType], dynamic_position: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], static_position: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExtractOp(source=source, dynamic_position=dynamic_position, static_position=static_position, results=results, loc=loc, ip=ip).result


def extract(condition: ArrayLike, arr: ArrayLike,
            *, size: int | None = None, fill_value: ArrayLike = 0) -> Array:
  """Return the elements of an array that satisfy a condition.

  JAX implementation of :func:`numpy.extract`.

  Args:
    condition: array of conditions. Will be converted to boolean and flattened to 1D.
    arr: array of values to extract. Will be flattened to 1D.
    size: optional static size for output. Must be specified in order for ``extract``
      to be compatible with JAX transformations like :func:`~jax.jit` or :func:`~jax.vmap`.
    fill_value: if ``size`` is specified, fill padded entries with this value (default: 0).

  Returns:
    1D array of extracted entries . If ``size`` is specified, the result will have shape
    ``(size,)`` and be right-padded with ``fill_value``. If ``size`` is not specified,
    the output shape will depend on the number of True entries in ``condition``.

  Notes:
    This function does not require strict shape agreement between ``condition`` and ``arr``.
    If ``condition.size > arr.size``, then ``condition`` will be truncated, and if
    ``arr.size > condition.size``, then ``arr`` will be truncated.

  See also:
    :func:`jax.numpy.compress`: multi-dimensional version of ``extract``.

  Examples:
     Extract values from a 1D array:

     >>> x = jnp.array([1, 2, 3, 4, 5, 6])
     >>> mask = (x % 2 == 0)
     >>> jnp.extract(mask, x)
     Array([2, 4, 6], dtype=int32)

     In the simplest case, this is equivalent to boolean indexing:

     >>> x[mask]
     Array([2, 4, 6], dtype=int32)

     For use with JAX transformations, you can pass the ``size`` argument to
     specify a static shape for the output, along with an optional ``fill_value``
     that defaults to zero:

     >>> jnp.extract(mask, x, size=len(x), fill_value=0)
     Array([2, 4, 6, 0, 0, 0], dtype=int32)

     Notice that unlike with boolean indexing, ``extract`` does not require strict
     agreement between the sizes of the array and condition, and will effectively
     truncate both to the minimum size:

     >>> short_mask = jnp.array([False, True])
     >>> jnp.extract(short_mask, x)
     Array([2], dtype=int32)
     >>> long_mask = jnp.array([True, False, True, False, False, False, False, False])
     >>> jnp.extract(long_mask, x)
     Array([1, 3], dtype=int32)
  """
  util.check_arraylike("extreact", condition, arr, fill_value)
  return compress(ravel(condition), ravel(arr), size=size, fill_value=fill_value)


def extract(
  f: tp.Callable[[jax.tree_util.KeyPath, tp.Any, tp.Any], bool],
  prefix: tp.Any,
  tree: tp.Any,
  *,
  is_leaf: tp.Callable[[tp.Any], bool] | None = None,
) -> tuple[tp.Any, list[tp.Any]]:
  extracted: list[tp.Any] = []
  def _leaf_fn(path: jax.tree_util.KeyPath, prefix_leaf: tp.Any, leaf: tp.Any):
    if f(path, prefix_leaf, leaf):
      idx = len(extracted)
      extracted.append(leaf)
      return ExtractIndex(idx)
    return leaf

  full_prefix = jax.tree.broadcast(prefix, tree, is_leaf=is_leaf)
  new_tree = jax.tree.map_with_path(_leaf_fn, full_prefix, tree, is_leaf=is_leaf)
  return new_tree, extracted

