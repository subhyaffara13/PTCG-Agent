
def unflatten(
    module: ExportedProgram, flat_args_adapter: FlatArgsAdapter | None = None
) -> UnflattenedModule:
    """Unflatten an ExportedProgram, producing a module with the same module
    hierarchy as the original eager module. This can be useful if you are trying
    to use :mod:`torch.export` with another system that expects a module
    hierarchy instead of the flat graph that :mod:`torch.export` usually produces.

    .. note:: The args/kwargs of unflattened modules will not necessarily match
        the eager module, so doing a module swap (e.g. :code:`self.submod =
        new_mod`) will not necessarily work. If you need to swap a module out, you
        need to set the :code:`preserve_module_call_signature` parameter of
        :func:`torch.export.export`.

    Args:
        module (ExportedProgram): The ExportedProgram to unflatten.
        flat_args_adapter (Optional[FlatArgsAdapter]): Adapt flat args if input TreeSpec does not match with exported module's.

    Returns:
        An instance of :class:`UnflattenedModule`, which has the same module
        hierarchy as the original eager module pre-export.
    """
    module = _remove_effect_tokens(module)
    m = UnflattenedModule(module, flat_args_adapter)

    # Disable process_forward_inputs as the adapter has many
    # non-dynamo-traceable behavior.
    m.process_forward_inputs = torch._dynamo.disable(  # type: ignore[method-assign]
        m.process_forward_inputs,
        reason="do not trace into preprocessing the inputs",
        recursive=True,
    )

    return m


def unflatten(a: TensorLikeType, dim: int, sizes: ShapeType) -> TensorLikeType:
    dim = utils.canonicalize_dim(a.ndim, dim)
    torch._check(len(sizes) != 0, lambda: "unflatten: sizes must be non-empty")
    return a.view(tuple(a.shape[:dim]) + tuple(sizes) + tuple(a.shape[dim + 1 :]))


def unflatten(g: jit_utils.GraphContext, input, dim, unflattened_size):
    input_dim = symbolic_helper._get_tensor_rank(input)
    if input_dim is None:
        return symbolic_helper._unimplemented(
            "dim",
            "ONNX and PyTorch use different strategies to split the input. "
            "Input rank must be known at export time.",
        )

    # dim could be negative
    input_dim = g.op("Constant", value_t=torch.tensor([input_dim], dtype=torch.int64))
    dim = g.op("Add", input_dim, dim)
    dim = g.op("Mod", dim, input_dim)

    input_size = g.op("Shape", input)

    head_start_idx = g.op("Constant", value_t=torch.tensor([0], dtype=torch.int64))
    head_end_idx = g.op(
        "Reshape", dim, g.op("Constant", value_t=torch.tensor([1], dtype=torch.int64))
    )
    head_part_rank = g.op("Slice", input_size, head_start_idx, head_end_idx)

    dim_plus_one = g.op(
        "Add", dim, g.op("Constant", value_t=torch.tensor([1], dtype=torch.int64))
    )
    tail_start_idx = g.op(
        "Reshape",
        dim_plus_one,
        g.op("Constant", value_t=torch.tensor([1], dtype=torch.int64)),
    )
    tail_end_idx = g.op(
        "Constant", value_t=torch.tensor([_constants.INT64_MAX], dtype=torch.int64)
    )
    tail_part_rank = g.op("Slice", input_size, tail_start_idx, tail_end_idx)

    final_shape = g.op(
        "Concat", head_part_rank, unflattened_size, tail_part_rank, axis_i=0
    )

    return symbolic_helper._reshape_helper(g, input, final_shape)


def unflatten(iter, n=2):
    """Group ``iter`` into tuples of length ``n``. Raise an error if
    the length of ``iter`` is not a multiple of ``n``.
    """
    if n < 1 or len(iter) % n:
        raise ValueError('iter length is not a multiple of %i' % n)
    return list(zip(*(iter[i::n] for i in range(n))))


def unflatten(
    separator: str = '.',
    *,
    inplace: bool = False,
    target: Any = None,
) -> Transformation:
  """Converts a flat dictionary with separated keys into a nested PyTree.

  Example:
      params = {
          'linear1.kernel.qvalue': arr1,
          'linear1.kernel.scale': arr2,
      }
      transform = unflatten()
      result = transform(params)
      # result = {
      #     'linear1': {
      #         'kernel': {
      #             'qvalue': arr1,
      #             'scale': arr2,
      #         }
      #     }
      # }

  Args:
      separator: The string used to separate keys.
      inplace: If True, deletes matched keys from input params to save memory.
        Requires input params to be a dict.
      target: A reference PyTree. If provided, the returned value will conform
        to this structure, and keys not in the target will be filtered out.

  Returns:
      A Transformation function.
  """

  def transform(
      *params: types.PyTreeOf[Any],
  ) -> types.PyTreeOf[Any]:
    assert (
        len(params) == 1
    ), 'Can only unflatten parameters in a single parameter structure.'
    p = params[0]
    if target is not None:
      flat_target = tree_utils.to_flat_dict(target, sep=separator)
      flat_p = p if isinstance(p, dict) else dict(p)
      missing_keys = set(flat_target.keys()) - set(flat_p.keys())
      if missing_keys:
        logging.warning(
            'The following %d keys were missing in the checkpoint and will'
            ' retain their default values: %s',
            len(missing_keys),
            list(missing_keys)[:10],
        )
      if inplace and isinstance(p, dict):
        for k, v in flat_target.items():
          if k not in p:
            p[k] = v
      else:
        p = dict(p)
        for k, v in flat_target.items():
          if k not in p:
            p[k] = v
    return tree_utils.from_flat_dict(
        p, target=target, sep=separator, inplace=inplace
    )

  return transform


def unflatten(treedef: tree_util.PyTreeDef,
              leaves: Iterable[tree_util.Leaf]) -> Any:
  """Reconstructs a pytree from the treedef and the leaves.

  The inverse of :func:`tree_flatten`.

  Args:
    treedef: the treedef to reconstruct
    leaves: the iterable of leaves to use for reconstruction. The iterable must
      match the leaves of the treedef.

  Returns:
    The reconstructed pytree, containing the ``leaves`` placed in the structure
    described by ``treedef``.

  Examples:
    >>> import jax
    >>> vals, treedef = jax.tree.flatten([1, (2, 3), [4, 5]])
    >>> newvals = [100, 200, 300, 400, 500]
    >>> jax.tree.unflatten(treedef, newvals)
    [100, (200, 300), [400, 500]]

  See Also:
    - :func:`jax.tree.flatten`
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.structure`
  """
  return tree_util.tree_unflatten(treedef, leaves)


def unflatten(xs: Iterable[T], ns: Sequence[int]) -> list[list[T]]:
  """Splits `xs` into subsequences of lengths `ns`.

  Unlike `split_list`, the `sum(ns)` must be equal to `len(xs)`."""
  xs_iter = iter(xs)
  unflattened = [[next(xs_iter) for _ in range(n)] for n in ns]
  assert next(xs_iter, _unflatten_done) is _unflatten_done
  return unflattened


def unflatten(space: Space[T], x: FlatType) -> T:
    """Unflatten a data point from a space.

    This reverses the transformation applied by :func:`flatten`. You must ensure
    that the ``space`` argument is the same as for the :func:`flatten` call.

    Args:
        space: The space used to unflatten ``x``
        x: The array to unflatten

    Returns:
        A point with a structure that matches the space.

    Raises:
        NotImplementedError: if the space is not defined in :mod:`gymnasium.spaces`.
    """
    raise NotImplementedError(f"Unknown space: `{space}`")


def unflatten(space: Space[T], x: FlatType) -> T:
    """Unflatten a data point from a space.

    This reverses the transformation applied by :func:`flatten`. You must ensure
    that the ``space`` argument is the same as for the :func:`flatten` call.

    Args:
        space: The space used to unflatten ``x``
        x: The array to unflatten

    Returns:
        A point with a structure that matches the space.

    Raises:
        NotImplementedError: if the space is not defined in ``gym.spaces``.
    """
    raise NotImplementedError(f"Unknown space: `{space}`")


def unflatten(  # type: ignore[invalid-annotation]
  graphdef: GraphDef[Node],
  state: State[Key, tp.Any] | FlatState[tp.Any] | list[tp.Any],
  /,
  *,
  index_ref: IndexMap | None = None,
  outer_index_outer_ref: IndexMap | None = None,
  copy_variables: bool = False,
  recreate_variables: bool = True,
) -> Node:
  """Unflattens a graphdef into a node with the given state.

  Args:
    graphdef: A GraphDef instance.
    state: A State instance.
    index_ref: A mapping from indexes to nodes references found during the graph
      traversal, defaults to None. If not provided, a new empty dictionary is
      created. This argument can be used to unflatten a sequence of (graphdef,
      state) pairs that share the same index space.
    index_ref_cache: A mapping from indexes to existing nodes that can be
      reused. When an reference is reused, ``GraphNodeImpl.clear`` is called to
      leave the object in an empty state and then filled by the unflatten
      process, as a result existing graph nodes are mutated to have the new
      content/topology specified by the graphdef.
    copy_variables: If True variables in the state will be copied onto the new
      new structure, else variables will be shared. Default is False.
  """
  if isinstance(state, (State, dict)):
    leaves = _get_sorted_leaves(state)
  elif isinstance(state, FlatState):
    leaves = state.leaves
  elif isinstance(state, list):  # type: ignore
    leaves = state
  else:
    raise ValueError(f'Unsupported state type: {type(state)}')

  if len(leaves) != graphdef.num_leaves:
    raise ValueError(
      f'Incorrect number of leaves, expected {graphdef.num_leaves} leaves, but got {len(leaves)}.'
    )

  if graphdef.nodes and isinstance(graphdef.nodes[0], TreeNodeDef):
    return _tree_unflatten(graphdef, leaves, copy_variables)

  if index_ref is None:
    index_ref = IndexMap()

  if len(graphdef.nodes) == 0:
    return leaves[0]
  elif isinstance(nodedef := graphdef.nodes[0], NodeRef):
    node = index_ref[nodedef.index]
  else:
    node_iter = iter(graphdef.nodes)
    attribute_iter = iter(graphdef.attributes)
    leaves_iter = iter(leaves)
    nodedef = next(node_iter)
    assert not isinstance(nodedef, NodeRef)
    if isinstance(nodedef, ArrayRefDef):
      node_impl = None
    else:
      node_impl = get_node_impl_for_type(nodedef.type)
    node = _graph_unflatten(
      nodedef,
      node_impl,
      node_iter,
      attribute_iter,
      leaves_iter,
      index_ref,
      outer_index_outer_ref,
      copy_variables,
      recreate_variables
    )

    try:
      next(leaves_iter)
    except StopIteration:
      pass
    else:
      raise ValueError('Incorrect number of leaves in state.')

  return node


def unflatten(array: _ArrayT, batch_shape: _Shape, pattern: str) -> _ArrayT:
  (array,) = einops.unpack(array, [batch_shape], pattern.replace('...', '*'))
  return array

