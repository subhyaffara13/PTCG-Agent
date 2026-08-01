
def map(
    f: Callable[[pytree.PyTree, tuple[pytree.PyTree, ...]], pytree.PyTree],
    xs: pytree.PyTree | torch.Tensor,
    *args: TypeVarTuple,
):
    r"""
    Performs a map of f with xs. Intuitively, you can think of the semantic being::

        out = []
        for idx in len(xs.size(0)):
            xs_sliced = xs.select(0, idx)
            out.append(f(xs_sliced, *args))
        torch.stack(out)

    .. warning::

        ``torch._higher_order_ops.map`` is a prototype feature in PyTorch. It currently
        does not support autograd and you may run into miscompiles.
        Read more about feature classification at:
        https://pytorch.org/blog/pytorch-feature-classification-changes/#prototype


    Args:
        f (Callable): a callable that takes an input x, that could either be a single Tensor
            or a nested dict, list of tensors and some additional inputs
        xs: the inputs that're to be mapped over. We'll iterate over the first dim of each x
            and perform f on each slice.

        *args: additional arguments provided to each step of f. They could also be omitted and
            map is able to automatically figure out the read dependency.

    Return:
        the stacked output for each step of f

    Example::

        def f(xs):
            return xs[0] + xs[1] + const1 + const2


        xs = [torch.randn(2, 3), torch.randn(2, 3)]
        const1 = torch.randn(2, 3)
        const2 = torch.randn(2, 3)
        # returns a tensor of shape [2, 2, 3]
        torch._higher_order_ops.map(f, xs)

    """
    flat_xs, xs_spec = pytree.tree_flatten(xs)
    flat_args, args_spec = pytree.tree_flatten(args)
    if not all(isinstance(t, torch.Tensor) for t in flat_xs):
        raise RuntimeError(f"Mapped xs can only consist of tensors. Got xs {flat_xs}.")

    shapes = [xs.shape for xs in flat_xs]
    leading_dim_size = shapes[0][0]
    if leading_dim_size == 0:
        raise RuntimeError("Leading dimensions of mapped xs cannot be 0.")

    if any(cur_shape[0] != leading_dim_size for cur_shape in shapes):
        raise RuntimeError(
            f"Leading dimensions of mapped xs must be consistent. Got shapes {shapes}."
        )

    def run_flattened_map(f, flat_xs, flat_args):
        def wrapped_fn(*flat_args, f, xs_tree_spec, args_tree_spec, num_xs):
            xs = pytree.tree_unflatten(flat_args[:num_xs], xs_tree_spec)
            args = pytree.tree_unflatten(flat_args[num_xs:], args_tree_spec)
            return f(xs, *args)

        inner_f = functools.partial(
            wrapped_fn,
            f=f,
            xs_tree_spec=xs_spec,
            args_tree_spec=args_spec,
            num_xs=len(flat_xs),
        )
        return map_impl(inner_f, flat_xs, flat_args)

    from torch._higher_order_ops.utils import _maybe_compile_and_run_fn

    return _maybe_compile_and_run_fn(run_flattened_map, f, flat_xs, flat_args)


def map(result: _ods_ir.Type, inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimensions: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MapOp(result=result, inputs=inputs, dimensions=dimensions, loc=loc, ip=ip).result


def map(result: _ods_ir.Type, inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MapOp(result=result, inputs=inputs, dimensions=dimensions, loc=loc, ip=ip).result


def map(f: Callable[..., Any],
        tree: Any,
        *rest: Any,
        is_leaf: Callable[[Any], bool] | None = None) -> Any:
  """Maps a multi-input function over pytree args to produce a new pytree.

  Args:
    f: function that takes ``1 + len(rest)`` arguments, to be applied at the
      corresponding leaves of the pytrees.
    tree: a pytree to be mapped over, with each leaf providing the first
      positional argument to ``f``.
    rest: a tuple of pytrees, each of which has the same structure as ``tree``
      or has ``tree`` as a prefix.
    is_leaf: an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    A new pytree with the same structure as ``tree`` but with the value at each
    leaf given by ``f(x, *xs)`` where ``x`` is the value at the corresponding
    leaf in ``tree`` and ``xs`` is the tuple of values at corresponding nodes in
    ``rest``.

  Examples:

    >>> import jax
    >>> jax.tree.map(lambda x: x + 1, {"x": 7, "y": 42})
    {'x': 8, 'y': 43}

    If multiple inputs are passed, the structure of the tree is taken from the
    first input; subsequent inputs need only have ``tree`` as a prefix:

    >>> jax.tree.map(lambda x, y: [x] + y, [5, 6], [[7, 9], [1, 2]])
    [[5, 7, 9], [6, 1, 2]]

  See Also:
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.reduce`
  """
  return tree_util.tree_map(f, tree, *rest, is_leaf=is_leaf)


def map(f, xs, *, batch_size: int | None = None):
  """Map a function over leading array axes.

  Like Python's builtin map, except inputs and outputs are in the form of
  stacked arrays. Consider using the :func:`~jax.vmap` transform instead, unless you
  need to apply a function element by element for reduced memory usage or
  heterogeneous computation with other control flow primitives.

  When ``xs`` is an array type, the semantics of :func:`~map` are given by this
  Python implementation::

    def map(f, xs):
      return np.stack([f(x) for x in xs])

  Like :func:`~scan`, :func:`~map` is implemented in terms of JAX primitives so
  many of the same advantages over a Python loop apply: ``xs`` may be an
  arbitrary nested pytree type, and the mapped computation is compiled only
  once.

  If ``batch_size`` is provided, the computation is executed in batches of that size
  and parallelized using :func:`~jax.vmap`. This can be used as either a more performant
  version of ``map`` or as a memory-efficient version of ``vmap``. If the axis is not
  divisible by the batch size, the remainder is processed in a separate ``vmap`` and
  concatenated to the result.

  ``batch_size=0`` is equivalent to applying a ``vmap``. That is, it uses a full batch.

    >>> x = jnp.ones((10, 3, 4))
    >>> def f(x):
    ...   print('inner shape:', x.shape)
    ...   return x + 1
    >>> y = lax.map(f, x, batch_size=3)
    inner shape: (3, 4)
    inner shape: (3, 4)
    >>> y.shape
    (10, 3, 4)

  In the example above, "inner shape" is printed twice, once while tracing the batched
  computation and once while tracing the remainder computation.

  Args:
    f: a Python function to apply element-wise over the first axis or axes of
      ``xs``.
    xs: values over which to map along the leading axis.
    batch_size: (optional) integer specifying the size of the batch for each step to execute
      in parallel.

  Returns:
    Mapped values.
  """
  if batch_size is not None:
    scan_xs, remainder_xs = _batch_and_remainder(xs, batch_size)
    g = lambda _, x: ((), api.vmap(f)(x))
    if scan_xs is not None:
      _, scan_ys = scan(g, (), scan_xs)
    else:
      scan_ys = None

    flatten = lambda x: x.reshape(-1, *x.shape[2:])
    if scan_ys is None:
      ys = api.vmap(f)(remainder_xs)
    elif remainder_xs is not None:
      remainder_ys = api.vmap(f)(remainder_xs)
      ys = tree_map(
        lambda x, y: lax.concatenate([flatten(x), y], dimension=0), scan_ys,
        remainder_ys)
    else:
      ys = tree_map(flatten, scan_ys)
  else:
    g = lambda _, x: ((), f(x))
    _, ys = scan(g, (), xs)
  return ys


def map(
    font, location, *, inputNormalized=False, outputNormalized=False, dropZeroes=False
):
    if "fvar" not in font:
        return None

    fvar = font["fvar"]
    axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in fvar.axes}
    unknownAxes = sorted(tag for tag in location if tag not in axes)
    if unknownAxes:
        raise ValueError(f"Unknown axis tag(s): {', '.join(unknownAxes)}")

    if not inputNormalized:
        location = {
            tag: normalizeValue(value, axes[tag]) for tag, value in location.items()
        }

    if "avar" in font:
        location = font["avar"].renormalizeLocation(location, font, dropZeroes)

    if not outputNormalized:
        location = {
            tag: _denormalize(value, axes[tag]) for tag, value in location.items()
        }

    return location


def map(
  f: tp.Callable[[tuple, tp.Any], tp.Any],
  node: A,
  /,
  *,
  graph: bool | None = None,
  recreate_variables: bool = True,
) -> A:
  """Map a function over the state of a graph node.

  ``map`` extracts the state from ``node`` using :func:`split`, applies ``f``
  to every ``(path, value)`` pair using :func:`map_state`, and returns a
  new node with the mapped values merged back into the original structure.
  Note that the leaves in the state are :class:`Variable` objects, so ``f``
  should handle them accordingly.

  Example usage::

    >>> from flax import nnx
    >>> import jax.numpy as jnp

    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> new_model = nnx.map(lambda path, v: v.replace(jnp.zeros_like(v)), model)
    >>> assert jnp.all(new_model.kernel[...] == 0)
    >>> assert jnp.all(new_model.bias[...] == 0)

  Args:
    f: A callable ``(path, value) -> new_value`` applied to each leaf in the
      state. ``path`` is a tuple of path parts and ``value`` is the
      corresponding leaf (typically a :class:`Variable`).
    node: A graph node object.
    graph: If ``True``, uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    A :class:`State` with the mapped values.
  """
  graphdef, state = split(node, graph=graph)
  state = statelib.map_state(f, state)
  return merge(graphdef, state, recreate_variables=recreate_variables)

