
def split(path, sep):
    if sep not in path:
        return "", path

    return path.rsplit(sep, 1)


def split(pattern, string, maxsplit=0, flags=0, concurrent=None, timeout=None,
  ignore_unused=False, **kwargs):
    """Split the source string by the occurrences of the pattern, returning a
    list containing the resulting substrings.  If capturing parentheses are used
    in pattern, then the text of all groups in the pattern are also returned as
    part of the resulting list.  If maxsplit is nonzero, at most maxsplit splits
    occur, and the remainder of the string is returned as the final element of
    the list."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.split(string, maxsplit, concurrent, timeout)


def split(
    tensor: Tensor,
    split_size_or_sections: int | list[int],
    dim: int = 0,
) -> tuple[Tensor, ...]:
    r"""Splits the tensor into chunks. Each chunk is a view of the original tensor.

    If :attr:`split_size_or_sections` is an integer type, then :attr:`tensor` will
    be split into equally sized chunks (if possible). Last chunk will be smaller if
    the tensor size along the given dimension :attr:`dim` is not divisible by
    :attr:`split_size`.

    If :attr:`split_size_or_sections` is a list, then :attr:`tensor` will be split
    into ``len(split_size_or_sections)`` chunks with sizes in :attr:`dim` according
    to :attr:`split_size_or_sections`.

    Args:
        tensor (Tensor): tensor to split.
        split_size_or_sections (int) or (list(int)): size of a single chunk or
            list of sizes for each chunk
        dim (int): dimension along which to split the tensor.

    Example::

        >>> a = torch.arange(10).reshape(5, 2)
        >>> a
        tensor([[0, 1],
                [2, 3],
                [4, 5],
                [6, 7],
                [8, 9]])
        >>> torch.split(a, 2)
        (tensor([[0, 1],
                 [2, 3]]),
         tensor([[4, 5],
                 [6, 7]]),
         tensor([[8, 9]]))
        >>> torch.split(a, [1, 4])
        (tensor([[0, 1]]),
         tensor([[2, 3],
                 [4, 5],
                 [6, 7],
                 [8, 9]]))
    """
    if has_torch_function_unary(tensor):
        return handle_torch_function(
            split, (tensor,), tensor, split_size_or_sections, dim=dim
        )
    # Overwriting reason:
    # This dispatches to two ATen functions depending on the type of
    # split_size_or_sections. The branching code is in _tensor.py, which we
    # call here.
    return tensor.split(split_size_or_sections, dim)


def split(x, device_mesh):
    """Split forward, all-gather backward."""
    return _Split.apply(x, device_mesh)


def split(key: torch.Tensor, num: int = 2) -> torch.Tensor:
    r"""Split a PRNG key into ``num`` new independent keys.

    Each returned key produces a different, deterministic random sequence.
    This is the primary mechanism for deriving multiple independent keys from
    a single parent key without mutating any state.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, each key in the
    batch is split independently and the result has shape ``(num, *batch, K)``.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        num (int): Number of keys to produce. Default: ``2``.

    Returns:
        A tensor of shape ``(num, *key.shape)`` containing the derived keys.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> k1, k2 = torch.func._random.split(key)  # doctest: +SKIP
    """
    return torch.ops.aten._philox_key_split(key, num)


def split(self: Tensor, split_size: int, dim: int = 0) -> tuple[Tensor, ...]:
    input_sizes = self.shape
    dim_size = input_sizes[dim]
    if split_size == 0:
        if dim_size != 0:
            raise AssertionError(
                f"split_size is 0 but dim_size is {dim_size}, expected 0"
            )
        return (self.detach(),)
    chunks = (dim_size + split_size - 1) // split_size

    # Avoid importing sympy at a module level
    from torch.fx.experimental.symbolic_shapes import guard_int

    chunks = guard_int(chunks)
    split_sizes = [split_size for i in range(chunks)]
    split_sizes[-1] = split_size - (split_size * chunks - dim_size)
    return torch.split(self, split_sizes, dim)


def split(x, sizes, dim=0):
    dim = _validate_dim(x, dim, 0)
    sizes_ = sizes

    # If sizes is an integer (or a SymInt), we turn it into a list of sizes
    # by computing what the actual size of each chunk should be.
    if not isinstance(sizes, (list, tuple)):
        x_size = x.get_size()[dim]
        chunks = V.graph.sizevars.guard_int(FloorDiv(x_size + sizes - 1, sizes))
        sizes_ = [sizes] * chunks
        # The last chunk might have a smaller size than the rest.
        sizes_[-1] = x_size - (chunks - 1) * sizes

    # From this point, we assume that the sum of the sizes of all chunks
    # equals the size of the base tensor.
    result = []
    start = 0
    for size in sizes_:
        end = start + size
        # No need for clamping here, since we compute the exact
        # start and end values.
        result.append(slice_(x, dim, start, end, clamp=False))
        start = end
    return result


def split(ary: ArrayLike, indices_or_sections, axis=0):
    return _split_helper(ary, indices_or_sections, axis, strict=True)


def split(g: jit_utils.GraphContext, self, split_size_or_sizes, dim, _outputs=None):
    if not symbolic_helper._is_split_static(split_size_or_sizes, _outputs):
        split_out = g.op("SplitToSequence", self, split_size_or_sizes, axis_i=dim)
        if _outputs is None:
            return split_out
        # Convert to multiple slice nodes iff number of splits and number of outputs are statically known.
        if (
            symbolic_helper._is_packed_list(split_size_or_sizes)
            and len(symbolic_helper._unpack_list(split_size_or_sizes)) == _outputs
        ):
            split_sizes = [
                symbolic_helper._unsqueeze_helper(g, v, [0])
                for v in symbolic_helper._unpack_list(split_size_or_sizes)
            ]
            start = g.op("Constant", value_t=torch.tensor([0], dtype=torch.long))
            axis = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
            res = []
            for i in range(_outputs):
                end = g.op(
                    "Add", start, split_sizes[i]
                )  # split_sizes is a list of same length as _outputs
                res.append(g.op("Slice", self, start, end, axis))
                start = end
            return res
        return [
            g.op(
                "SequenceAt",
                split_out,
                g.op("Constant", value_t=torch.tensor([i], dtype=torch.long)),
            )
            for i in range(_outputs)
        ]
    else:
        return opset9.split(g, self, split_size_or_sizes, dim, _outputs)


def split(g: jit_utils.GraphContext, self, split_size_or_sizes, dim, _outputs=None):
    if not symbolic_helper._is_split_static(split_size_or_sizes, _outputs):
        split_out = g.op("SplitToSequence", self, split_size_or_sizes, axis_i=dim)
        if _outputs is None:
            return split_out
        # Convert to multiple slice nodes iff number of splits and number of outputs are statically known.
        if (
            symbolic_helper._is_packed_list(split_size_or_sizes)
            and len(symbolic_helper._unpack_list(split_size_or_sizes)) == _outputs
        ):
            split_sizes = [
                symbolic_helper._unsqueeze_helper(g, v, [0])
                for v in symbolic_helper._unpack_list(split_size_or_sizes)
            ]

            start = g.op("Constant", value_t=torch.tensor([0], dtype=torch.long))
            axis = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
            res = []
            for i in range(_outputs):
                end = g.op(
                    "Add", start, split_sizes[i]
                )  # split_sizes is a list of same length as _outputs
                res.append(g.op("Slice", self, start, end, axis))
                start = end
            return res
        return [
            g.op(
                "SequenceAt",
                split_out,
                g.op("Constant", value_t=torch.tensor([i], dtype=torch.long)),
            )
            for i in range(_outputs)
        ]

    split_val = symbolic_helper._node_get(split_size_or_sizes.node(), "value")
    if split_val.dim() > 0:
        # pyrefly: ignore [bad-argument-type]
        return g.op("Split", self, split_size_or_sizes, axis_i=dim, outputs=_outputs)
    split_size = symbolic_helper._get_const(split_size_or_sizes, "i", "split_size")

    size = symbolic_helper._get_tensor_dim_size(self, dim)
    if size is None:
        if _outputs is not None:
            size = split_size * _outputs
        else:
            raise errors.SymbolicValueError(
                "Unknown dimension size not supported", self
            )
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    splits = g.op("Constant", value_t=torch.tensor(splits))
    # pyrefly: ignore [bad-argument-type]
    return g.op("Split", self, splits, axis_i=dim, outputs=_outputs)


def split(g: jit_utils.GraphContext, self, split_size_or_sizes, dim, _outputs=None):
    if not symbolic_helper._is_split_static(split_size_or_sizes, _outputs):
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "split", 9, 11, "Dynamic number of outputs not supported", self
        )
    split_val = symbolic_helper._node_get(split_size_or_sizes.node(), "value")
    if split_val.dim() > 0:
        return split_with_sizes(g, self, split_size_or_sizes, dim, _outputs)
    split_size = symbolic_helper._get_const(split_size_or_sizes, "i", "split_size")

    size = symbolic_helper._get_tensor_dim_size(self, dim)
    if size is None:
        if _outputs is not None:
            size = split_size * _outputs
        else:
            return symbolic_helper._onnx_opset_unsupported_detailed(
                "split", 9, 11, "Unknown dimension size not supported", self
            )
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    # pyrefly: ignore [bad-argument-type]
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=_outputs)


def split(ary, indices_or_sections, axis=0):
    """
    Split an array into multiple sub-arrays as views into `ary`.

    Parameters
    ----------
    ary : ndarray
        Array to be divided into sub-arrays.
    indices_or_sections : int or 1-D array
        If `indices_or_sections` is an integer, N, the array will be divided
        into N equal arrays along `axis`.  If such a split is not possible,
        an error is raised.

        If `indices_or_sections` is a 1-D array of sorted integers, the entries
        indicate where along `axis` the array is split.  For example,
        ``[2, 3]`` would, for ``axis=0``, result in

        - ary[:2]
        - ary[2:3]
        - ary[3:]

        If an index exceeds the dimension of the array along `axis`,
        an empty sub-array is returned correspondingly.
    axis : int, optional
        The axis along which to split, default is 0.

    Returns
    -------
    sub-arrays : list of ndarrays
        A list of sub-arrays as views into `ary`.

    Raises
    ------
    ValueError
        If `indices_or_sections` is given as an integer, but
        a split does not result in equal division.

    See Also
    --------
    array_split : Split an array into multiple sub-arrays of equal or
                  near-equal size.  Does not raise an exception if
                  an equal division cannot be made.
    hsplit : Split array into multiple sub-arrays horizontally (column-wise).
    vsplit : Split array into multiple sub-arrays vertically (row wise).
    dsplit : Split array into multiple sub-arrays along the 3rd axis (depth).
    concatenate : Join a sequence of arrays along an existing axis.
    stack : Join a sequence of arrays along a new axis.
    hstack : Stack arrays in sequence horizontally (column wise).
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).

    Examples
    --------
    >>> import numpy as np
    >>> x = np.arange(9.0)
    >>> np.split(x, 3)
    [array([0.,  1.,  2.]), array([3.,  4.,  5.]), array([6.,  7.,  8.])]

    >>> x = np.arange(8.0)
    >>> np.split(x, [3, 5, 6, 10])
    [array([0.,  1.,  2.]),
     array([3.,  4.]),
     array([5.]),
     array([6.,  7.]),
     array([], dtype=float64)]

    """
    try:
        len(indices_or_sections)
    except TypeError:
        sections = indices_or_sections
        N = ary.shape[axis]
        if N % sections:
            raise ValueError(
                'array split does not result in an equal division') from None
    return array_split(ary, indices_or_sections, axis)


def split(config_path: str) -> Tuple[Any]:
  """Returns config_path split into a tuple of parts.

  Example usage:
    >>> assert config_path.split('a.b.cc') == ('a', 'b', 'cc')
    >>> assert config_path.split('a.b["cc.d"]') == ('a', 'b', 'cc.d')
    >>> assert config_path.split('a.b[10]') == ('a', 'b', 10)
    >>> assert config_path.split('a[(1, 2)]') == ('a', (1, 2))
    >>> assert config_path.split('a[:]') == ('a', slice(None))

  Args:
    config_path: Input path to be split - see example usage.

  Returns:
    Tuple of config_path split into parts. Parts are attributes or subscripts.
    Attrributes are treated as strings and subscripts are parsed using
    ast.literal_eval. It is up to the caller to ensure all returned types are
    valid.

  Raises:
    ValueError: Failed to parse config_path.
  """
  try:
    node = ast.parse(config_path, mode='eval')
  except SyntaxError as e:
    raise ValueError(f'Could not parse {config_path!r}: {e!r}') from None
  if isinstance(node, ast.Expression):
    result = _split_node(node.body)
    if isinstance(result, tuple):
      return result
  raise ValueError(config_path)


def split(src: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return SplitOp(src=src, results=results, loc=loc, ip=ip).results


def split(operand: ArrayLike, sizes: Sequence[DimSize],
          axis: int = 0) -> Sequence[Array]:
  """Splits an array along ``axis``.

  Args:
    operand: an array to split
    sizes: the sizes of the split arrays. The sum of the sizes must be equal
      to the size of the ``axis`` dimension of ``operand``.
    axis: the axis along which to split the array.

  Returns:
    A sequence of ``len(sizes)`` arrays. If ``sizes`` is
    ``[s1, s2, ...]``, this function returns chunks of sizes ``s1``, ``s2``,
    taken along ``axis``.
  """
  operand = asarray(operand)
  return split_p.bind(operand, sizes=tuple(sizes),
                      axis=canonicalize_axis(axis, operand.ndim))


def split(ary: ArrayLike, indices_or_sections: int | Sequence[int] | ArrayLike,
          axis: int = 0) -> list[Array]:
  """Split an array into sub-arrays.

  JAX implementation of :func:`numpy.split`.

  Args:
    ary: N-dimensional array-like object to split
    indices_or_sections: either a single integer or a sequence of indices.

      - if ``indices_or_sections`` is an integer *N*, then *N* must evenly divide
        ``ary.shape[axis]`` and ``ary`` will be divided into *N* equally-sized
        chunks along ``axis``.
      - if ``indices_or_sections`` is a sequence of integers, then these integers
        specify the boundary between unevenly-sized chunks along ``axis``; see
        examples below.

    axis: the axis along which to split; defaults to 0.

  Returns:
    A list of arrays. If ``indices_or_sections`` is an integer *N*, then the list is
    of length *N*. If ``indices_or_sections`` is a sequence *seq*, then the list is
    is of length *len(seq) + 1*.

  Examples:
    Splitting a 1-dimensional array:

    >>> x = jnp.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    Split into three equal sections:

    >>> chunks = jnp.split(x, 3)
    >>> print(*chunks)
    [1 2 3] [4 5 6] [7 8 9]

    Split into sections by index:

    >>> chunks = jnp.split(x, [2, 7])  # [x[0:2], x[2:7], x[7:]]
    >>> print(*chunks)
    [1 2] [3 4 5 6 7] [8 9]

    Splitting a two-dimensional array along axis 1:

    >>> x = jnp.array([[1, 2, 3, 4],
    ...                [5, 6, 7, 8]])
    >>> x1, x2 = jnp.split(x, 2, axis=1)
    >>> print(x1)
    [[1 2]
     [5 6]]
    >>> print(x2)
    [[3 4]
     [7 8]]

  See also:
    - :func:`jax.numpy.array_split`: like ``split``, but allows ``indices_or_sections``
      to be an integer that does not evenly divide the size of the array.
    - :func:`jax.numpy.vsplit`: split vertically, i.e. along axis=0
    - :func:`jax.numpy.hsplit`: split horizontally, i.e. along axis=1
    - :func:`jax.numpy.dsplit`: split depth-wise, i.e. along axis=2
  """
  return _split("split", ary, indices_or_sections, axis=axis)


def split(key: ArrayLike, num: int | tuple[int, ...] = 2) -> Array:
  """Splits a PRNG key into `num` new keys by adding a leading axis.

  Args:
    key: a PRNG key (from ``key``, ``split``, ``fold_in``).
    num: optional, a positive integer (or tuple of integers) indicating
      the number (or shape) of keys to produce. Defaults to 2.

  Returns:
    An array-like object of `num` new PRNG keys.
  """
  typed_key, wrapped = _check_prng_key("split", key)
  return _return_prng_keys(wrapped, _split(typed_key, num))


def split(tensor: Any, split_size_or_sections: Any, dim: Any = None) -> tuple:
    """
    Split tensor along a dimension.

    Can handle both regular integer sizes and Dim objects for split sizes.
    When Dim objects are used, they get bound to the resulting tensor dimensions.
    """
    from ._wrap import _wrap_dim

    # Check if dim is a Dim object
    dim_is_object = isinstance(dim, Dim)

    # Parse split_size_or_sections
    if isinstance(split_size_or_sections, int):
        # Single integer - use regular split
        if dim_is_object:
            raise TypeError(
                "when dim is specified as a Dim object, split sizes must also be dimensions."
            )
        return _Tensor._torch_function_fallback(
            torch.Tensor.split,
            (type(tensor),),
            (tensor, split_size_or_sections),
            {"dim": dim},
        )

    # Check if it's a sequence
    sizes = []
    all_dims = True
    all_ints = True

    for item in split_size_or_sections:
        sizes.append(item)
        if isinstance(item, Dim):
            all_ints = False
        else:
            all_dims = False

    if all_ints:
        # All integers - use regular split
        if dim_is_object:
            raise TypeError(
                "when dim is specified as a Dim object, split sizes must also be dimensions."
            )
        return _Tensor._torch_function_fallback(
            torch.Tensor.split,
            (type(tensor),),
            (tensor, split_size_or_sections),
            {"dim": dim},
        )

    if not all_dims:
        raise TypeError("split list must be ints or dims but got a mix")

    # All are Dim objects - handle first-class dimension split
    self_info = TensorInfo.create(tensor, ensure_batched=False, ensure_present=False)
    ndim = self_info.ndim()

    if not dim_is_object and ndim == 0:
        raise TypeError("split expects at least a 1-dimension tensor")

    # Wrap the dimension
    dim_l = _wrap_dim(dim, ndim, False) if dim is not None else DimEntry(-ndim)

    # Find the index of the dimension in levels
    idx = None
    for i, level in enumerate(self_info.levels):
        if level == dim_l:
            idx = i
            break

    if idx is None:
        if dim is None:
            dim = 0
        raise TypeError(f"tensor does not contain dimension {dim}")

    # Calculate split indices
    indices = []
    total_size = 0
    unbound = []

    for i, size_dim in enumerate(sizes):
        if size_dim.is_bound:
            indices.append(size_dim.size)
            total_size += indices[-1]
        else:
            indices.append(0)
            unbound.append(i)

    if self_info.tensor is None:
        raise AssertionError("Cannot get tensor size on None tensor")
    tensor_size = self_info.tensor.size(idx)

    # Handle unbound dimensions
    if unbound:
        if total_size > tensor_size:
            raise TypeError(
                f"sizes of target dimensions add up to more ({total_size}) than source dim ({tensor_size})"
            )
        remaining_size = tensor_size - total_size
        chunk_size = (remaining_size + len(unbound) - 1) // len(unbound)
        for u in unbound:
            sz = min(chunk_size, remaining_size)
            sizes[u].size = sz
            indices[u] = sz
            remaining_size -= sz
    elif tensor_size != total_size:
        raise TypeError(
            f"sum of sizes of target dimensions ({total_size}) do not match the source dim ({tensor_size})"
        )

    # Perform the split
    result_tensors = self_info.tensor.split_with_sizes(indices, idx)

    # Create result with new levels
    result = []
    new_levels = list(self_info.levels)

    for i, (result_tensor, size_dim) in enumerate(zip(result_tensors, sizes)):
        new_levels[idx] = DimEntry(size_dim)
        result.append(
            Tensor.from_positional(
                result_tensor, list(new_levels), self_info.has_device
            )
        )

    return tuple(result)


def split(path: str) -> tuple[str, str]:
    if "/" not in path:
        return ("", path)
    split = path.rsplit("/", 1)
    return (split[0] or "/", split[1])


def split(  # type: ignore[invalid-annotation]
  graph_node: A, /, *, graph: bool | None = None,
) -> tuple[GraphDef[A], State]: ...


def split(  # type: ignore[invalid-annotation]
  graph_node: A, first: filterlib.Filter, /, *, graph: bool | None = None,
) -> tuple[GraphDef[A], State]: ...


def split(  # type: ignore[invalid-annotation]
  graph_node: A,
  first: filterlib.Filter,
  second: filterlib.Filter,
  /,
  *filters: filterlib.Filter,
  graph: bool | None = None,
) -> tuple[
  GraphDef[A],
  State,
  tpe.Unpack[tuple[State, ...]],
]: ...


def split(  # type: ignore[invalid-annotation]
  node: A, *filters: filterlib.Filter, graph: bool | None = None,
) -> tuple[
  GraphDef[A],
  State,
  tpe.Unpack[tuple[State, ...]],
]:
  """Split a graph node into a :class:`GraphDef` and one or more :class:`State`s. State is
  a ``Mapping`` from strings or integers to ``Variables``, Arrays or nested States. GraphDef
  contains all the static information needed to reconstruct a ``Module`` graph, it is analogous
  to JAX's ``PyTreeDef``. :func:`split` is used in conjunction with :func:`merge` to switch
  seamlessly between stateful and stateless representations of the graph.

  Example usage::

    >>> from flax import nnx
    >>> import jax, jax.numpy as jnp
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.batch_norm = nnx.BatchNorm(2, rngs=rngs)
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...
    >>> node = Foo(nnx.Rngs(0))
    >>> graphdef, params, batch_stats = nnx.split(node, nnx.Param, nnx.BatchStat)
    ...
    >>> jax.tree.map(jnp.shape, params)
    State({
      'batch_norm': {
        'bias': Param(
          value=(2,)
        ),
        'scale': Param(
          value=(2,)
        )
      },
      'linear': {
        'bias': Param(
          value=(3,)
        ),
        'kernel': Param(
          value=(2, 3)
        )
      }
    })
    >>> jax.tree.map(jnp.shape, batch_stats)
    State({
      'batch_norm': {
        'mean': BatchStat(
          value=(2,)
        ),
        'var': BatchStat(
          value=(2,)
        )
      }
    })

  :func:`split` and :func:`merge` are primarily used to interact directly with JAX
  transformations, see
  `Functional API <https://flax.readthedocs.io/en/latest/nnx/nnx_basics.html#the-functional-api>`__
  for more information.

  Arguments:
    node: graph node to split.
    *filters: some optional filters to group the state into mutually exclusive substates.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    ``GraphDef`` and one or more ``States`` equal to the number of filters passed. If no
    filters are passed, a single ``State`` is returned.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  graphdef, flat_state = flatten(node, graph=graph)
  flat_states = _split_state(flat_state, filters)
  states = _to_nested_state(graphdef, flat_states)
  return graphdef, *states  # type: ignore[return-value]

