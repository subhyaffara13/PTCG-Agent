from typing import Any, Callable
import math


def flatten(x):
    f = cStringIO.StringIO()
    _flatten(x, f)
    return f.getvalue()


def flatten(seq, scalarp=is_scalar_or_string):
    """
    Return a generator of flattened nested containers.

    For example:

        >>> from matplotlib.cbook import flatten
        >>> l = (('John', ['Hunter']), (1, 23), [[([42, (5, 23)], )]])
        >>> print(list(flatten(l)))
        ['John', 'Hunter', 1, 23, 42, 5, 23]

    By: Composite of Holger Krekel and Luther Blissett
    From: https://code.activestate.com/recipes/121294-simple-generator-for-flattening-nested-containers/
    and Recipe 1.12 in cookbook
    """  # noqa: E501
    for item in seq:
        if scalarp(item) or item is None:
            yield item
        else:
            yield from flatten(item, scalarp)


def flatten(t: Expression) -> list[Expression]:
    """Flatten a nested sequence of tuples/lists into one list of nodes."""
    if isinstance(t, (TupleExpr, ListExpr)):
        return [b for a in t.items for b in flatten(a)]
    elif isinstance(t, StarExpr):
        return flatten(t.expr)
    else:
        return [t]


def flatten(arr: list):
    res = []
    if len(arr) > 0:
        for sub_arr in arr:
            if isinstance(arr[0], (list, tuple)):
                res.extend(flatten(sub_arr))
            else:
                res.append(sub_arr)
    return res


def flatten(index, name="segmented_flatten"):
    """
    Flattens a batched index map (which is typically of shape batch_size, seq_length) to a 1d index map. This operation
    relabels the segments to keep batch elements distinct. The k-th batch element will have indices shifted by
    *num_segments* * (k - 1). The result is a tensor with *num_segments* multiplied by the number of elements in the
    batch.

    Args:
        index (`IndexMap`):
            IndexMap to flatten.
        name (`str`, *optional*, defaults to 'segmented_flatten'):
            Name for the operation. Currently not used

    Returns:
        (`IndexMap`): The flattened IndexMap.
    """
    # first, get batch_size as scalar tensor
    batch_size = torch.prod(torch.tensor(list(index.batch_shape())))
    # next, create offset as 1-D tensor of length batch_size,
    # and multiply element-wise by num segments (to offset different elements in the batch) e.g. if batch size is 2: [0, 64]
    offset = torch.arange(start=0, end=batch_size, device=index.num_segments.device) * index.num_segments
    offset = offset.view(index.batch_shape())
    for _ in range(index.batch_dims, len(index.indices.size())):  # typically range(1,2)
        offset = offset.unsqueeze(-1)

    indices = offset + index.indices
    return IndexMap(indices=indices.view(-1), num_segments=index.num_segments * batch_size, batch_dims=0)


def flatten(input: list[int], start_dim: int, end_dim: int):
    start_dim = maybe_wrap_dim(start_dim, len(input))
    end_dim = maybe_wrap_dim(end_dim, len(input))
    if start_dim > end_dim:
        raise AssertionError(f"Expected start_dim ({start_dim}) <= end_dim ({end_dim})")
    if len(input) == 0:
        return [1]
    if start_dim == end_dim:
        # TODO: return self
        out: list[int] = []
        for elem in input:
            out.append(elem)
        return out
    slice_numel = 1
    for i in range(start_dim, end_dim + 1):
        slice_numel *= input[i]
    # TODO: use slicing when slice optimization has landed
    # slice_numel = multiply_integers(input[start_dim:end_dim - start_dim + 1])
    shape: list[int] = []
    for i in range(start_dim):
        shape.append(input[i])
    shape.append(slice_numel)
    for i in range(end_dim + 1, len(input)):
        shape.append(input[i])
    return shape


def flatten(a: TensorLikeType, start_dim: int = 0, end_dim: int = -1) -> TensorLikeType:
    start_dim = utils.canonicalize_dim(a.ndim, start_dim)
    end_dim = utils.canonicalize_dim(a.ndim, end_dim)

    # Short-circuits on no-op
    if start_dim == end_dim and a.ndim != 0:
        return a

    # Tries to take a view
    # TODO: we could look at directing collapse_view to skip its meta function here (unsafe_collapse_view)
    # Unbacked semantics: if validity of in-place flattening is undecided we copy.
    new_shape, _new_strides = prims._collapse_view_helper(
        a, start_dim, end_dim, must_be_valid=None
    )
    if new_shape is not None:
        return prims.collapse_view(a, start_dim, end_dim)

    # Makes a copy if it can't make a view
    return prims.collapse(a, start_dim, end_dim)


def flatten(g: jit_utils.GraphContext, input, start_dim, end_dim):
    dim = symbolic_helper._get_tensor_rank(input)
    if dim == 1:
        return input
    # use ONNX's Flatten operator for cases where the output shape is 2D
    if start_dim == 1:
        if end_dim == -1 or (dim is not None and end_dim == dim - 1):
            return g.op("Flatten", input, axis_i=start_dim)
    elif start_dim == 0:
        if end_dim == -2 or (dim is not None and end_dim == dim - 2):
            return g.op("Flatten", input, axis_i=end_dim + 1)
    if dim is None:
        return symbolic_helper._unimplemented(
            "dim",
            "ONNX and PyTorch use different strategies to split the input. "
            "Input rank must be known at export time.",
        )
    # if end_dim is negative add dim
    if end_dim < 0:
        end_dim = dim + end_dim

    return symbolic_helper._flatten_helper(g, input, start_dim, end_dim, dim)


def flatten(g: jit_utils.GraphContext, input, start_dim, end_dim):
    start_dim_i = symbolic_helper._get_const(start_dim, "i", "start_dim")
    end_dim_i = symbolic_helper._get_const(end_dim, "i", "end_dim")

    dim = input.type().dim()
    if end_dim_i < 0:
        end_dim_i = dim + end_dim_i
    # use ONNX's Flatten operator for cases where the output shape is 2D
    if start_dim_i == 1 and end_dim_i == dim - 1:
        if symbolic_helper._try_get_scalar_type(input):
            old_type, input = _try_cast_integer_to_float(g, input)
            return _cast_to_type(
                g, g.op("Flatten", input, axis_i=start_dim_i), old_type
            )
        else:
            return g.op("Flatten", input, axis_i=start_dim_i)
    if start_dim_i == 0 and end_dim_i == dim - 2:
        if symbolic_helper._try_get_scalar_type(input):
            old_type, input = _try_cast_integer_to_float(g, input)
            return _cast_to_type(
                g, g.op("Flatten", input, axis_i=end_dim_i + 1), old_type
            )
        else:
            return g.op("Flatten", input, axis_i=end_dim_i + 1)

    return opset9.flatten(g, input, start_dim, end_dim)


def flatten(g: jit_utils.GraphContext, input, start_dim, end_dim):
    dim = symbolic_helper._get_tensor_rank(input)
    if dim is None:
        return symbolic_helper._unimplemented(
            "dim",
            "ONNX and PyTorch use different strategies to split the input. "
            "Input rank must be known at export time.",
            input,
        )

    if dim == 0:
        return symbolic_helper._reshape_helper(g, input, [1])
    if dim == 1:
        return g.op("Identity", input)
    # TODO: remove this as onnx opset 11 spec allows negative axes
    if end_dim < 0:
        end_dim = dim + end_dim
    # use ONNX's Flatten operator for cases where the output shape is 2D
    if start_dim == 1 and end_dim == dim - 1:
        return g.op("Flatten", input, axis_i=start_dim)
    if start_dim == 0 and end_dim == dim - 2:
        return g.op("Flatten", input, axis_i=end_dim + 1)

    return symbolic_helper._flatten_helper(g, input, start_dim, end_dim, dim)


def flatten(t: IntTuple) -> tuple[int, ...]:
    if is_tuple(t):
        if len(t) == 0:
            return ()
        else:
            return tuple(i for a in t for i in flatten(a))
    else:
        return (t,)


def flatten(expr, new=new):
    """ Flatten T(a, b, T(c, d), T2(e)) to T(a, b, c, d, T2(e)) """
    cls = expr.__class__
    args = []
    for arg in expr.args:
        if arg.__class__ == cls:
            args.extend(arg.args)
        else:
            args.append(arg)
    return new(expr.__class__, *args)


def flatten(iterable, levels=None, cls=None):  # noqa: F811
    """
    Recursively denest iterable containers.

    >>> from sympy import flatten

    >>> flatten([1, 2, 3])
    [1, 2, 3]
    >>> flatten([1, 2, [3]])
    [1, 2, 3]
    >>> flatten([1, [2, 3], [4, 5]])
    [1, 2, 3, 4, 5]
    >>> flatten([1.0, 2, (1, None)])
    [1.0, 2, 1, None]

    If you want to denest only a specified number of levels of
    nested containers, then set ``levels`` flag to the desired
    number of levels::

    >>> ls = [[(-2, -1), (1, 2)], [(0, 0)]]

    >>> flatten(ls, levels=1)
    [(-2, -1), (1, 2), (0, 0)]

    If cls argument is specified, it will only flatten instances of that
    class, for example:

    >>> from sympy import Basic, S
    >>> class MyOp(Basic):
    ...     pass
    ...
    >>> flatten([MyOp(S(1), MyOp(S(2), S(3)))], cls=MyOp)
    [1, 2, 3]

    adapted from https://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
    """
    from sympy.tensor.array import NDimArray
    if levels is not None:
        if not levels:
            return iterable
        elif levels > 0:
            levels -= 1
        else:
            raise ValueError(
                "expected non-negative number of levels, got %s" % levels)

    if cls is None:
        def reducible(x):
            return is_sequence(x, set)
    else:
        def reducible(x):
            return isinstance(x, cls)

    result = []

    for el in iterable:
        if reducible(el):
            if hasattr(el, 'args') and not isinstance(el, NDimArray):
                el = el.args
            result.extend(flatten(el, levels=levels, cls=cls))
        else:
            result.append(el)

    return result


def flatten(listOfLists):
    """Return an iterator flattening one level of nesting in a list of lists.

        >>> list(flatten([[0, 1], [2, 3]]))
        [0, 1, 2, 3]

    See also :func:`collapse`, which can flatten multiple levels of nesting.

    """
    return chain.from_iterable(listOfLists)


def flatten(line):
    """
    Flatten an arbitrarily nested sequence.

    Parameters
    ----------
    line : sequence
        The non string sequence to flatten

    Notes
    -----
    This doesn't consider strings sequences.

    Returns
    -------
    flattened : generator
    """
    for element in line:
        if iterable_not_string(element):
            yield from flatten(element)
        else:
            yield element


def flatten(data: dict) -> list[tuple[str, Any]]:
    """Flatten create_pickle_data"""
    return [
        (typ, example)
        for typ, examples in data.items()
        for example in examples.values()
    ]


def flatten(
    inner: base.GradientTransformation,
) -> base.GradientTransformationExtraArgs:
  """Flattens parameters and gradients for init and update of inner transform.

  This can reduce the overhead of performing many calculations on lots of small
  variables, at the cost of slightly increased memory usage.

  Args:
    inner: Inner transformation to flatten inputs for.

  Returns:
    New :class:`optax.GradientTransformationExtraArgs`
  """

  inner = base.with_extra_args_support(inner)

  def _flatten(params):
    """Flattens and concatenates all tensors in params to a single vector."""
    params, _ = jax.tree.flatten(params)
    return jnp.concatenate([jnp.reshape(param, [-1]) for param in params])

  def _unflatten(updates, flat):
    """Extracts tensors from flat, using the structure and shapes of params."""
    updates_flat, treedef = jax.tree.flatten(updates)
    offsets = []
    for update in updates_flat:
      size = np.size(update)
      if offsets:
        offsets.append(size + offsets[-1])
      else:
        offsets.append(size)
    del offsets[-1]
    flat_split = jnp.split(flat, offsets)
    reshaped = [
        jnp.reshape(flat_update, update.shape)
        for flat_update, update in zip(flat_split, updates_flat)
    ]
    return jax.tree.unflatten(treedef, reshaped)

  def init_fn(params):
    flat = _flatten(params)
    return inner.init(flat)

  def update_fn(updates, state, params=None, **extra_args):
    if params is not None:
      params = _flatten(params)
    updates_flat, state = inner.update(
        _flatten(updates), state, params, **extra_args
    )
    updates = _unflatten(updates, updates_flat)
    return updates, state

  return base.GradientTransformationExtraArgs(init_fn, update_fn)


def flatten(x: chex.Array) -> chex.Array:
  """Flattens the array, i.e. reshapes it in a 1D shape."""
  return x.reshape(-1)


def flatten(*lists):
  return [item for sublist in lists for item in sublist]


def flatten(t: Iterable[Iterable[_T]]) -> list[_T]:
    return [item for sublist in t for item in sublist]


def flatten(inputs):
    return [[flatten(i) for i in inputs] if isinstance(inputs, (list, tuple)) else inputs]


def flatten(obj, result=None):
    """Return flattened version of (possibly nested) iterable object."""
    if not isinstance(obj, Iterable | Sized) or isinstance(obj, str):
        return obj
    if result is None:
        result = []
    for item in obj:
        if not isinstance(item, Iterable | Sized) or isinstance(item, str):
            result.append(item)
        else:
            flatten(item, result)
    return tuple(result)


def Flatten():
  """Layer construction function for flattening all but the leading dim."""
  def init_fun(rng, input_shape):
    output_shape = input_shape[0], math.prod(input_shape[1:])
    return output_shape, ()
  def apply_fun(params, inputs, **kwargs):
    return jnp.reshape(inputs, (inputs.shape[0], -1))
  return init_fun, apply_fun


def flatten(tree: Any,
            is_leaf: Callable[[Any], bool] | None = None
            ) -> tuple[list[tree_util.Leaf], tree_util.PyTreeDef]:
  """Flattens a pytree.

  The flattening order (i.e. the order of elements in the output list)
  is deterministic, corresponding to a left-to-right depth-first tree
  traversal.

  Args:
    tree: a pytree to flatten.
    is_leaf: an optionally specified function that will be called at each
      flattening step. It should return a boolean, with true stopping the
      traversal and the whole subtree being treated as a leaf, and false
      indicating the flattening should traverse the current object.

  Returns:
    A pair where the first element is a list of leaf values and the second
    element is a treedef representing the structure of the flattened tree.

  Examples:
    >>> import jax
    >>> vals, treedef = jax.tree.flatten([1, (2, 3), [4, 5]])
    >>> vals
    [1, 2, 3, 4, 5]
    >>> treedef
    PyTreeDef([*, (*, *), [*, *]])

  See Also:
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.structure`
    - :func:`jax.tree.unflatten`
  """
  return tree_util.tree_flatten(tree, is_leaf)


def flatten(space: Space[T], x: T) -> FlatType:
    """Flatten a data point from a space.

    This is useful when e.g. points from spaces must be passed to a neural
    network, which only understands flat arrays of floats.

    Args:
        space: The space that ``x`` is flattened by
        x: The value to flatten

    Returns:
        The flattened datapoint

            - For :class:`gymnasium.spaces.Box` and :class:`gymnasium.spaces.MultiBinary`, this is a flattened array
            - For :class:`gymnasium.spaces.Discrete` and :class:`gymnasium.spaces.MultiDiscrete`, this is a flattened one-hot array of the sample
            - For :class:`gymnasium.spaces.Tuple` and :class:`gymnasium.spaces.Dict`, this is a concatenated array the subspaces (does not support graph subspaces)
            - For graph spaces, returns :class:`GraphInstance` where:
                - :attr:`GraphInstance.nodes` are n x k arrays
                - :attr:`GraphInstance.edges` are either:
                    - m x k arrays
                    - None
                - :attr:`GraphInstance.edge_links` are either:
                    - m x 2 arrays
                    - None

    Raises:
        NotImplementedError: If the space is not defined in :mod:`gymnasium.spaces`.

    Example:
        >>> from gymnasium.spaces import Box, Discrete, Tuple
        >>> space = Box(0, 1, shape=(3, 5))
        >>> flatten(space, space.sample()).shape
        (15,)
        >>> space = Discrete(4)
        >>> flatten(space, 2)
        array([0, 0, 1, 0])
        >>> space = Tuple((Box(0, 1, shape=(2,)), Box(0, 1, shape=(3,)), Discrete(3)))
        >>> example = ((.5, .25), (1., 0., .2), 1)
        >>> flatten(space, example)
        array([0.5 , 0.25, 1.  , 0.  , 0.2 , 0.  , 1.  , 0.  ])
    """
    raise NotImplementedError(f"Unknown space: `{space}`")


def flatten(space: Space[T], x: T) -> FlatType:
    """Flatten a data point from a space.

    This is useful when e.g. points from spaces must be passed to a neural
    network, which only understands flat arrays of floats.

    Args:
        space: The space that ``x`` is flattened by
        x: The value to flatten

    Returns:
        - For ``Box`` and ``MultiBinary``, this is a flattened array
        - For ``Discrete`` and ``MultiDiscrete``, this is a flattened one-hot array of the sample
        - For ``Tuple`` and ``Dict``, this is a concatenated array the subspaces (does not support graph subspaces)
        - For graph spaces, returns `GraphInstance` where:
            - `nodes` are n x k arrays
            - `edges` are either:
                - m x k arrays
                - None
            - `edge_links` are either:
                - m x 2 arrays
                - None

    Raises:
        NotImplementedError: If the space is not defined in ``gym.spaces``.
    """
    raise NotImplementedError(f"Unknown space: `{space}`")


def flatten(  # type: ignore[invalid-annotation]
  node: Node,
  /,
  *,
  ref_index: RefMap | None = ...,
  ref_outer_index: RefMap | None = ...,
  graph: bool = ...,
) -> tuple[GraphDef[Node], FlatState[tp.Any]]: ...


def flatten(  # type: ignore[invalid-annotation]
  node: Node,
  /,
  *,
  with_paths: tp.Literal[True],
  ref_index: RefMap | None = ...,
  ref_outer_index: RefMap | None = ...,
  graph: bool = ...,
) -> tuple[
  GraphDef[Node],
  FlatState[tp.Any],
]: ...


def flatten(  # type: ignore[invalid-annotation]
  node: Node,
  /,
  *,
  with_paths: tp.Literal[False],
  ref_index: RefMap | None = ...,
  ref_outer_index: RefMap | None = ...,
  graph: bool = ...,
) -> tuple[
  GraphDef[Node],
  list[tp.Any],
]: ...


def flatten(  # type: ignore[invalid-annotation]
  node: Node,
  /,
  *,
  with_paths: bool,
  ref_index: RefMap | None = ...,
  ref_outer_index: RefMap | None = ...,
  graph: bool = ...,
) -> tuple[
  GraphDef[Node],
  FlatState[tp.Any] | list[tp.Any],
]: ...


def flatten(  # type: ignore[invalid-annotation]
  node: Node,
  /,
  *,
  with_paths: bool = True,
  ref_index: RefMap | None = None,
  ref_outer_index: RefMap | None = None,
  graph: bool | None = None,
) -> tuple[
  GraphDef[Node],
  FlatState[tp.Any] | list[tp.Any],
]:
  """Flattens a graph node into a (graphdef, state) pair.

  Args:
    x: A graph node.
    ref_index: A mapping from nodes to indexes, defaults to None. If not provided, a new
      empty dictionary is created. This argument can be used to flatten a sequence of graph
      nodes that share references.
    with_paths: A boolean that indicates whether to return a FlatState object that includes
      the paths, or just a list of the Variable's inner values.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  if ref_index is None:
    ref_index = RefMap()
  leaves: list[tp.Any] = []
  path: list[Key] | None = [] if with_paths else None
  paths: list[PathParts] | None = [] if with_paths else None
  nodes: list[NodeDefType[tp.Any]] = []
  attributes: list[tuple[Key, AttrType]] = []
  if graph:
    node_impl = get_node_impl(node)
    _graph_flatten(
      node,
      node_impl,
      path,
      ref_index,
      ref_outer_index,
      nodes,
      attributes,
      leaves,
      paths,
    )
  else:
    _tree_flatten(
      node,
      nodes,
      leaves,
      paths,
    )
  graphdef: GraphDef = GraphDef(
    nodes=nodes, attributes=attributes, num_leaves=len(leaves)
  )

  if paths is not None:
    return graphdef, FlatState.from_sorted_keys_values(tuple(paths), leaves)  # type: ignore[return-value]
  else:
    return graphdef, leaves


def flatten(array: _ArrayT, pattern: str) -> tuple[_ArrayT, _Shape]:
  """Flatten an array along custom dimensions.

  Uses `einops` syntax.

  ```python
  flat_x, batch_shape = enp.flatten(x, '... h w c')
  y = enp.unflatten(y, batch_shape, '... h w c')
  ```

  * `x.shape == (h, w, c)`       -> `flat_x.shape == (1, h, w, c)`
  * `x.shape == (b, h, w, c)`    -> `flat_x.shape == (b, h, w, c)`
  * `x.shape == (b, n, h, w, c)` -> `flat_x.shape == (b * n, h, w, c)`

  Args:
    array: Array to flatten.
    pattern: Einops pattern to flatten the array.

  Returns:
    Tuple of (flattened array, batch shape).
  """
  array, (batch_shape,) = einops.pack([array], pattern.replace('...', '*'))
  return array, tuple(batch_shape)

