from typing import Callable, Union

def partition(n, seq, pad=no_pad):
    """ Partition sequence into tuples of length n

    >>> list(partition(2, [1, 2, 3, 4]))
    [(1, 2), (3, 4)]

    If the length of ``seq`` is not evenly divisible by ``n``, the final tuple
    is dropped if ``pad`` is not specified, or filled to length ``n`` by pad:

    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

    >>> list(partition(2, [1, 2, 3, 4, 5], pad=None))
    [(1, 2), (3, 4), (5, None)]

    See Also:
        partition_all
    """
    args = [iter(seq)] * n
    if pad is no_pad:
        return zip(*args)
    else:
        return zip_longest(*args, fillvalue=pad)


def partition(it, part):
    """ Partition a tuple/list into pieces defined by indices.

    Examples
    ========

    >>> from sympy.unify.core import partition
    >>> partition((10, 20, 30, 40), [[0, 1, 2], [3]])
    ((10, 20, 30), (40,))
    """
    return type(it)([index(it, ind) for ind in part])


def partition(n, k=None, zeros=False):
    """
    Returns a generator that can be used to generate partitions of an integer
    `n`.

    Explanation
    ===========

    A partition of `n` is a set of positive integers which add up to `n`. For
    example, partitions of 3 are 3, 1 + 2, 1 + 1 + 1. A partition is returned
    as a tuple. If ``k`` equals None, then all possible partitions are returned
    irrespective of their size, otherwise only the partitions of size ``k`` are
    returned. If the ``zero`` parameter is set to True then a suitable
    number of zeros are added at the end of every partition of size less than
    ``k``.

    ``zero`` parameter is considered only if ``k`` is not None. When the
    partitions are over, the last `next()` call throws the ``StopIteration``
    exception, so this function should always be used inside a try - except
    block.

    Details
    =======

    ``partition(n, k)``: Here ``n`` is a positive integer and ``k`` is the size
    of the partition which is also positive integer.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import partition
    >>> f = partition(5)
    >>> next(f)
    (1, 1, 1, 1, 1)
    >>> next(f)
    (1, 1, 1, 2)
    >>> g = partition(5, 3)
    >>> next(g)
    (1, 1, 3)
    >>> next(g)
    (1, 2, 2)
    >>> g = partition(5, 3, zeros=True)
    >>> next(g)
    (0, 0, 5)

    """
    if not zeros or k is None:
        for i in ordered_partitions(n, k):
            yield tuple(i)
    else:
        for m in range(1, k + 1):
            for i in ordered_partitions(n, m):
                i = tuple(i)
                yield (0,)*(k - len(i)) + i


def partition(pred, iterable):
    """
    Returns a 2-tuple of iterables derived from the input iterable.
    The first yields the items that have ``pred(item) == False``.
    The second yields the items that have ``pred(item) == True``.

        >>> is_odd = lambda x: x % 2 != 0
        >>> iterable = range(10)
        >>> even_items, odd_items = partition(is_odd, iterable)
        >>> list(even_items), list(odd_items)
        ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])

    If *pred* is None, :func:`bool` is used.

        >>> iterable = [0, 1, False, True, '', ' ']
        >>> false_items, true_items = partition(None, iterable)
        >>> list(false_items), list(true_items)
        ([0, False, ''], [1, True, ' '])

    """
    if pred is None:
        pred = bool

    t1, t2, p = tee(iterable, 3)
    p1, p2 = tee(map(pred, p))
    return (compress(t1, map(not_, p1)), compress(t2, p2))


def partition(
    a: Array,
    kth: int,
    /,
    axis: int | None = -1,
    *,
    xp: ModuleType | None = None,
) -> Array:
    """
    Return a partitioned copy of an array.

    Creates a copy of the array and partially sorts it in such a way that the value
    of the element in k-th position is in the position it would be in a sorted array.
    In the output array, all elements smaller than the k-th element are located to
    the left of this element and all equal or greater are located to its right.
    The ordering of the elements in the two partitions on the either side of
    the k-th element in the output array is undefined.

    Parameters
    ----------
    a : Array
        Input array.
    kth : int
        Element index to partition by.
    axis : int, optional
        Axis along which to partition. The default is ``-1`` (the last axis).
        If ``None``, the flattened array is used.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    partitioned_array
        Array of the same type and shape as `a`.

    Notes
    -----
    If `xp` implements ``partition`` or an equivalent function
    (e.g. ``topk`` for torch), complexity will likely be O(n).
    If not, this function simply calls ``xp.sort`` and complexity is O(n log n).
    """
    # Validate inputs.
    if xp is None:
        xp = array_namespace(a)
    if a.ndim < 1:
        msg = "`a` must be at least 1-dimensional"
        raise TypeError(msg)
    if axis is None:
        return partition(xp.reshape(a, (-1,)), kth, axis=0, xp=xp)
    (size,) = eager_shape(a, axis)
    if not (0 <= kth < size):
        msg = f"kth(={kth}) out of bounds [0 {size})"
        raise ValueError(msg)

    # Delegate where possible.
    if is_numpy_namespace(xp) or is_cupy_namespace(xp) or is_jax_namespace(xp):
        return xp.partition(a, kth, axis=axis)

    # Use top-k when possible:
    if is_torch_namespace(xp):
        if not (axis == -1 or axis == a.ndim - 1):
            a = xp.transpose(a, axis, -1)

        out = xp.empty_like(a)
        ranks = xp.arange(a.shape[-1]).expand_as(a)

        split_value, indices = xp.kthvalue(a, kth + 1, keepdim=True)
        del indices  # indices won't be used => del ASAP to reduce peak memory usage

        # fill the left-side of the partition
        mask_src = a < split_value
        n_left = mask_src.sum(dim=-1, keepdim=True)
        mask_dest = ranks < n_left
        out[mask_dest] = a[mask_src]

        # fill the middle of the partition
        mask_src = a == split_value
        n_left += mask_src.sum(dim=-1, keepdim=True)
        mask_dest ^= ranks < n_left
        out[mask_dest] = a[mask_src]

        # fill the right-side of the partition
        mask_src = a > split_value
        mask_dest = ranks >= n_left
        out[mask_dest] = a[mask_src]

        if not (axis == -1 or axis == a.ndim - 1):
            out = xp.transpose(out, axis, -1)
        return out

    # Note: dask topk/argtopk sort the return values, so it's
    # not much more efficient than sorting everything when
    # kth is not small compared to x.size

    return _funcs.partition(a, kth, axis=axis, xp=xp)


def partition(  # numpydoc ignore=PR01,RT01
    x: Array,
    kth: int,  # noqa: ARG001
    /,
    axis: int = -1,
    *,
    xp: ModuleType,
) -> Array:
    """See docstring in `array_api_extra._delegation.py`."""
    return xp.sort(x, axis=axis, stable=False)


def partition(
    pred: Callable[[T], bool], iterable: Iterable[T]
) -> tuple[Iterable[T], Iterable[T]]:
    """
    Use a predicate to partition entries into false entries and true entries,
    like

        partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    """
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def partition(
    classifier: Callable[[T], C],
    structure: PartsOf[T],
) -> Mapping[C, PartsOf[T]]:
  """Partitions a PartsOf[T] based on a leaf classifier function.

  Args:
    classifier: A function that assigns a class label to each leaf of the
      structure.
    structure: The structure to partition.

  Returns:
    A mapping from classification result to a PartsOf[T] containing only the
    values that were classified as such.

  Example:
    ```
    template = MyDataclass(a=(X, X), b={'c': X, 'd': X})
    t = PartsOf(template, MyDataclass(a=(1, 2), b={'c': 4, 'd': 3}))
    # Split the structure into one with even and another with odd values.
    even_odd = partition(lambda x: x % 2, t)

    assert even_odd[0].unsafe_structure == (
        MyDataclass(a=(..., 2), b={'c': 4, 'd': ...}
    )
    assert even_odd[1].unsafe_structure == (
        MyDataclass(a=(1, ...), b={'c': ...,' d': 3}
    )
    ```
  """
  value_paths_by_class = collections.defaultdict(set)
  for k, v in structure._present.items():  # pylint:disable=protected-access
    c = classifier(v)
    value_paths_by_class[c].add(k)
  return {
      c: filter_values(structure, value_paths)
      for c, value_paths in value_paths_by_class.items()
  }


def partition(
    transforms: Mapping[Hashable, base.GradientTransformation],
    param_labels: Union[base.PyTree, Callable[[base.PyTree], base.PyTree]],
    *,
    mask_compatible_extra_args: bool = False,
) -> base.GradientTransformationExtraArgs:
  """Partitions params and applies a different transformation to each subset.

  Sometimes you may want to apply different transformations to different
  parameters. For example, you may want to apply Adam to the weights of a
  neural network, but SGD to the biases. This function allows you to do that.

  Args:
    transforms: A mapping from labels to transformations. Each transformation
      will be only be applied to parameters with the same label.
    param_labels: A PyTree that is the same shape or a prefix of the
      parameters/updates (or a function that returns one given the parameters as
      input). The leaves of this PyTree correspond to the keys of the transforms
      (therefore the values at the leaves must be a subset of the keys).
    mask_compatible_extra_args: Whether to also apply the same masking to
      extra_arg fields with the same tree structure as params/updates.

  Returns:
    A :func:`optax.GradientTransformationExtraArgs` that implements an ``init``
    and ``update`` function.

  Examples:

    Below is an example where we apply Adam to the weights and SGD to the biases
    of a 2-layer neural network::

      >>> import optax
      >>> import jax
      >>> import jax.numpy as jnp

      >>> def map_nested_fn(fn):
      ...   '''Recursively apply `fn` to key-value pairs of a nested dict.'''
      ...   def map_fn(nested_dict):
      ...     return {k: (map_fn(v) if isinstance(v, dict) else fn(k, v))
      ...             for k, v in nested_dict.items()}
      ...   return map_fn

      >>> params = {'linear_1': {'w': jnp.zeros((5, 6)), 'b': jnp.zeros(5)},
      ...           'linear_2': {'w': jnp.zeros((6, 1)), 'b': jnp.zeros(1)}}
      >>> gradients = jax.tree.map(jnp.ones_like, params)  # dummy gradients

      >>> label_fn = map_nested_fn(lambda k, _: k)
      >>> tx = optax.partition(
      ...     {'w': optax.adam(1.0), 'b': optax.sgd(1.0)}, label_fn)
      >>> state = tx.init(params)
      >>> updates, new_state = tx.update(gradients, state, params)
      >>> new_params = optax.apply_updates(params, updates)

    Instead of providing a ``label_fn``, you may provide a PyTree of labels
    directly.  Also, this PyTree may be a prefix of the parameters PyTree. This
    is demonstrated in the GAN pseudocode below::

      >>> generator_params = ...
      >>> discriminator_params = ...
      >>> all_params = (generator_params, discriminator_params)
      >>> param_labels = ('generator', 'discriminator')

      >>> tx = optax.partition(
      >>>     {'generator': optax.adam(0.1), 'discriminator': optax.adam(0.5)},
      >>>     param_labels)

    If you would like to not optimize some parameters, you may wrap
    :func:`optax.partition` with :func:`optax.masked`.
  """

  transforms = {
      k: base.with_extra_args_support(v) for k, v in transforms.items()
  }

  def make_mask(labels, group):
    return jax.tree.map(lambda label: label == group, labels)

  def init_fn(params):
    labels = param_labels(params) if callable(param_labels) else param_labels

    label_set = set(jax.tree.leaves(labels))
    if not label_set.issubset(transforms.keys()):
      raise ValueError(
          'Some parameters have no corresponding transformation.\n'
          f'Parameter labels: {list(sorted(label_set))} \n'
          f'Transforms keys: {list(sorted(transforms.keys()))} \n'
      )

    inner_states = {
        group: wrappers.masked(
            tx,
            make_mask(labels, group),
            mask_compatible_extra_args=mask_compatible_extra_args,
        ).init(params)
        for group, tx in transforms.items()
    }
    return PartitionState(inner_states)

  def update_fn(updates, state, params=None, **extra_args):
    labels = param_labels(updates) if callable(param_labels) else param_labels
    new_inner_state = {}
    for group, tx in transforms.items():
      masked_tx = wrappers.masked(
          tx,
          make_mask(labels, group),
          mask_compatible_extra_args=mask_compatible_extra_args,
      )
      updates, new_inner_state[group] = masked_tx.update(
          updates, state.inner_states[group], params, **extra_args
      )
    return updates, PartitionState(new_inner_state)

  return base.GradientTransformationExtraArgs(init_fn, update_fn)


def partition(a, sep):
    """
    Partition each element in `a` around `sep`.

    Calls :meth:`str.partition` element-wise.

    For each element in `a`, split the element as the first
    occurrence of `sep`, and return 3 strings containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, return 3 strings
    containing the string itself, followed by two empty strings.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array
    sep : {str, unicode}
        Separator to split each string element in `a`.

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input types. The output array will have an extra
        dimension with 3 elements per input element.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array(["Numpy is nice!"])
    >>> np.char.partition(x, " ")
    array([['Numpy', ' ', 'is nice!']], dtype='<U8')

    See Also
    --------
    str.partition

    """
    return np.stack(strings_partition(a, sep), axis=-1)


def partition(a, kth, axis=-1, kind='introselect', order=None):
    """
    Return a partitioned copy of an array.

    Creates a copy of the array and partially sorts it in such a way that
    the value of the element in k-th position is in the position it would be
    in a sorted array. In the output array, all elements smaller than the k-th
    element are located to the left of this element and all equal or greater
    are located to its right. The ordering of the elements in the two
    partitions on the either side of the k-th element in the output array is
    undefined.

    Parameters
    ----------
    a : array_like
        Array to be sorted.
    kth : int or sequence of ints
        Element index to partition by. The k-th value of the element
        will be in its final sorted position and all smaller elements
        will be moved before it and all equal or greater elements behind
        it. The order of all elements in the partitions is undefined. If
        provided with a sequence of k-th it will partition all elements
        indexed by k-th  of them into their sorted position at once.

    axis : int or None, optional
        Axis along which to sort. If None, the array is flattened before
        sorting. The default is -1, which sorts along the last axis.
    kind : {'introselect'}, optional
        Selection algorithm. Default is 'introselect'.
    order : str or list of str, optional
        When `a` is an array with fields defined, this argument
        specifies which fields to compare first, second, etc.  A single
        field can be specified as a string.  Not all fields need be
        specified, but unspecified fields will still be used, in the
        order in which they come up in the dtype, to break ties.

    Returns
    -------
    partitioned_array : ndarray
        Array of the same type and shape as `a`.

    See Also
    --------
    ndarray.partition : Method to sort an array in-place.
    argpartition : Indirect partition.
    sort : Full sorting

    Notes
    -----
    The various selection algorithms are characterized by their average
    speed, worst case performance, work space size, and whether they are
    stable. A stable sort keeps items with the same key in the same
    relative order. The available algorithms have the following
    properties:

    ================= ======= ============= ============ =======
       kind            speed   worst case    work space  stable
    ================= ======= ============= ============ =======
    'introselect'        1        O(n)           0         no
    ================= ======= ============= ============ =======

    All the partition algorithms make temporary copies of the data when
    partitioning along any but the last axis.  Consequently,
    partitioning along the last axis is faster and uses less space than
    partitioning along any other axis.

    The sort order for complex numbers is lexicographic. If both the
    real and imaginary parts are non-nan then the order is determined by
    the real parts except when they are equal, in which case the order
    is determined by the imaginary parts.

    The sort order of ``np.nan`` is bigger than ``np.inf``.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([7, 1, 7, 7, 1, 5, 7, 2, 3, 2, 6, 2, 3, 0])
    >>> p = np.partition(a, 4)
    >>> p
    array([0, 1, 2, 1, 2, 5, 2, 3, 3, 6, 7, 7, 7, 7]) # may vary

    ``p[4]`` is 2;  all elements in ``p[:4]`` are less than or equal
    to ``p[4]``, and all elements in ``p[5:]`` are greater than or
    equal to ``p[4]``.  The partition is::

        [0, 1, 2, 1], [2], [5, 2, 3, 3, 6, 7, 7, 7, 7]

    The next example shows the use of multiple values passed to `kth`.

    >>> p2 = np.partition(a, (4, 8))
    >>> p2
    array([0, 1, 2, 1, 2, 3, 3, 2, 5, 6, 7, 7, 7, 7])

    ``p2[4]`` is 2  and ``p2[8]`` is 5.  All elements in ``p2[:4]``
    are less than or equal to ``p2[4]``, all elements in ``p2[5:8]``
    are greater than or equal to ``p2[4]`` and less than or equal to
    ``p2[8]``, and all elements in ``p2[9:]`` are greater than or
    equal to ``p2[8]``.  The partition is::

        [0, 1, 2, 1], [2], [3, 3, 2], [5], [6, 7, 7, 7, 7]
    """
    if axis is None:
        # flatten returns (1, N) for np.matrix, so always use the last axis
        a = asanyarray(a).flatten()
        axis = -1
    else:
        a = asanyarray(a).copy(order="K")
    a.partition(kth, axis=axis, kind=kind, order=order)
    return a


def partition(a, sep):
    """
    Partition each element in ``a`` around ``sep``.

    For each element in ``a``, split the element at the first
    occurrence of ``sep``, and return a 3-tuple containing the part
    before the separator, the separator itself, and the part after
    the separator. If the separator is not found, the first item of
    the tuple will contain the whole string, and the second and third
    ones will be the empty string.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array
    sep : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Separator to split each string element in ``a``.

    Returns
    -------
    out : 3-tuple:
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          part before the separator
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          separator
        - array with ``StringDType``, ``bytes_`` or ``str_`` dtype with the
          part after the separator

    See Also
    --------
    str.partition

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array(["Numpy is nice!"])
    >>> np.strings.partition(x, " ")
    (array(['Numpy'], dtype='<U5'),
     array([' '], dtype='<U1'),
     array(['is nice!'], dtype='<U8'))

    """
    a = np.asanyarray(a)
    sep = np.asanyarray(sep)

    if np.result_type(a, sep).char == "T":
        return _partition(a, sep)

    sep = sep.astype(a.dtype, copy=False)
    pos = _find_ufunc(a, sep, 0, MAX)
    a_len = str_len(a)
    sep_len = str_len(sep)

    not_found = pos < 0
    buffersizes1 = np.where(not_found, a_len, pos)
    buffersizes3 = np.where(not_found, 0, a_len - pos - sep_len)

    out_dtype = ",".join([f"{a.dtype.char}{n}" for n in (
        buffersizes1.max(),
        1 if np.all(not_found) else sep_len.max(),
        buffersizes3.max(),
    )])
    shape = np.broadcast_shapes(a.shape, sep.shape)
    out = np.empty_like(a, shape=shape, dtype=out_dtype)
    return _partition_index(a, sep, pos, out=(out["f0"], out["f1"], out["f2"]))


def partition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  """Returns a partially-sorted copy of an array.

  JAX implementation of :func:`numpy.partition`. The JAX version differs from
  NumPy in the treatment of NaN entries: NaNs which have the negative bit set
  are sorted to the beginning of the array.

  Args:
    a: array to be partitioned.
    kth: static integer index about which to partition the array.
    axis: static integer axis along which to partition the array; default is -1.

  Returns:
    A copy of ``a`` partitioned at the ``kth`` value along ``axis``. The entries
    before ``kth`` are values smaller than ``take(a, kth, axis)``, and entries
    after ``kth`` are indices of values larger than ``take(a, kth, axis)``

  Note:
    The JAX version requires the ``kth`` argument to be a static integer rather than
    a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
    you're only accessing the top or bottom k values of the output, it may be more
    efficient to call :func:`jax.lax.top_k` directly.

  See Also:
    - :func:`jax.numpy.sort`: full sort
    - :func:`jax.numpy.argpartition`: indirect partial sort
    - :func:`jax.lax.top_k`: directly find the top k entries
    - :func:`jax.lax.approx_max_k`: compute the approximate top k entries
    - :func:`jax.lax.approx_min_k`: compute the approximate bottom k entries

  Examples:
    >>> x = jnp.array([6, 8, 4, 3, 1, 9, 7, 5, 2, 3])
    >>> kth = 4
    >>> x_partitioned = jnp.partition(x, kth)
    >>> x_partitioned
    Array([1, 2, 3, 3, 4, 9, 8, 7, 6, 5], dtype=int32)

    The result is a partially-sorted copy of the input. All values before ``kth``
    are of smaller than the pivot value, and all values after ``kth`` are larger
    than the pivot value:

    >>> smallest_values = x_partitioned[:kth]
    >>> pivot_value = x_partitioned[kth]
    >>> largest_values = x_partitioned[kth + 1:]
    >>> print(smallest_values, pivot_value, largest_values)
    [1 2 3 3] 4 [9 8 7 6 5]

    Notice that among ``smallest_values`` and ``largest_values``, the returned
    order is arbitrary and implementation-dependent.
  """
  # TODO(jakevdp): handle NaN values like numpy.
  arr = util.ensure_arraylike("partition", a)
  if dtypes.issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.partition for complex dtype is not implemented.")
  axis = canonicalize_axis(axis, arr.ndim)
  kth = canonicalize_axis(kth, arr.shape[axis])

  arr = arr.swapaxes(axis, -1)
  if dtypes.isdtype(arr.dtype, "unsigned integer"):
    # Here, we apply a trick to handle correctly 0 values for unsigned integers
    bottom = -lax.top_k(-(arr + 1), kth + 1)[0] - 1
  else:
    bottom = -lax.top_k(-arr, kth + 1)[0]
  top = lax.top_k(arr, arr.shape[-1] - kth - 1)[0]
  out = lax.concatenate([bottom, top], dimension=arr.ndim - 1)
  return out.swapaxes(-1, axis)

