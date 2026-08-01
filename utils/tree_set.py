
def tree_set(root):
    return {
        os.path.join(os.path.relpath(dirpath, root), filename)
        for dirpath, dirnames, filenames in os.walk(root)
        for filename in filenames
    }


def tree_set(
    tree: base.PyTree,
    filtering: Optional[Callable[[_KeyPath, Any], bool]] = None,
    /,
    **kwargs: Any,
) -> base.PyTree:
  # pylint: disable=line-too-long
  r"""Creates a copy of tree with some values replaced as specified by kwargs.

  Search in the ``tree`` for ``keys`` in ``**kwargs`` (which can be a key
  from a dictionary, a field from a NamedTuple or the name of a NamedTuple).
  If such a key is found, replace the corresponding value with the one given in
  ``**kwargs``.

  Raises a ``KeyError`` if some keys in ``**kwargs`` are not present in the
  tree.

  Args:
    tree: pytree whose values are to be replaced.
    filtering: optional callable to further filter values in ``tree`` that match
      the keys to replace. ``filtering(path: Key_Path, value: Any) -> bool:
      ...`` takes as arguments both the path to the value (as returned by
      :func:`optax.tree_utils.tree_get_all_with_path`) and the value that match
      a given key.
    **kwargs: dictionary of keys with values to replace in ``tree``.

  Returns:
    new_tree
      new pytree with the same structure as ``tree``. For each element in
      ``tree`` whose key/field matches a key in ``**kwargs``, its value is
      set by the corresponding value in ``**kwargs``.

  Raises:
    KeyError: If no values of some key in ``**kwargs`` are found in ``tree``
      or none of the values satisfy the filtering operation.

  Examples:

    Basic usage

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.adam(learning_rate=1.)
      >>> state = opt.init(params)
      >>> print(state)
      (ScaleByAdamState(count=Array(0, dtype=int32), mu=Array([0., 0., 0.], dtype=float32), nu=Array([0., 0., 0.], dtype=float32)), EmptyState())
      >>> new_state = optax.tree_utils.tree_set(state, count=2.)
      >>> print(new_state)
      (ScaleByAdamState(count=2.0, mu=Array([0., 0., 0.], dtype=float32), nu=Array([0., 0., 0.], dtype=float32)), EmptyState())

    Usage with a filtering operation

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.inject_hyperparams(optax.sgd)(
      ...     learning_rate=lambda count: 1/(count+1)
      ...  )
      >>> state = opt.init(params)
      >>> print(state)
      InjectStatefulHyperparamsState(count=Array(0, dtype=int32), hyperparams={'learning_rate': Array(1., dtype=float32)}, hyperparams_states={'learning_rate': WrappedScheduleState(count=Array(0, dtype=int32))}, inner_state=(EmptyState(), EmptyState()))
      >>> filtering = lambda path, value: isinstance(value, jnp.ndarray)
      >>> new_state = optax.tree_utils.tree_set(
      ...   state, filtering, learning_rate=jnp.asarray(0.1)
      ... )
      >>> print(new_state)
      InjectStatefulHyperparamsState(count=Array(0, dtype=int32), hyperparams={'learning_rate': Array(0.1, dtype=float32, weak_type=True)}, hyperparams_states={'learning_rate': WrappedScheduleState(count=Array(0, dtype=int32))}, inner_state=(EmptyState(), EmptyState()))

  .. note:: The recommended usage to inject hyperparameters schedules is through
    :func:`optax.inject_hyperparams`. This function is a helper for other
    purposes.

  .. seealso:: :func:`optax.tree_utils.tree_get_all_with_path`,
    :func:`optax.tree_utils.tree_get`

  .. versionadded:: 0.2.2
  """  # noqa: E501
  # pylint: enable=line-too-long

  # First check if the keys are present in the tree
  for key in kwargs:
    found_values_with_path = tree_get_all_with_path(tree, key, filtering)
    if not found_values_with_path:
      if filtering:
        raise KeyError(
            f"Found no values matching '{key}' given the filtering operation in"
            f" {tree}"
        )
      raise KeyError(f"Found no values matching '{key}' in {tree}")

  has_any_key = functools.partial(_node_has_keys, keys=tuple(kwargs.keys()))

  def _replace(path: _KeyPath, node: Any) -> Any:
    """Replace a node with a new node whose values are updated."""
    if has_any_key(node):
      if (
          _is_named_tuple(node)
          and (node.__class__.__name__ in kwargs)
          and (filtering is None or filtering(path, node))
      ):
        # The node itself is a named tuple we wanted to replace
        return kwargs[node.__class__.__name__]
      # The node contains one of the keys we want to replace
      children_with_path = _get_children_with_path(path, node)
      new_children_with_keys = {}
      for child_path, child in children_with_path:
        # Scan each child of that node
        key = _get_key(child_path[-1])
        if key in kwargs and (
            filtering is None or filtering(child_path, child)
        ):
          # If the child matches a given key given the filtering operation
          # replaces with the new value
          new_children_with_keys.update({key: kwargs[key]})
        else:
          if isinstance(child, (dict, list, tuple)):
            # If the child is itself a pytree, further search in the child to
            # replace the given value
            new_children_with_keys.update({key: _replace(child_path, child)})
          else:
            # If the child is just a leaf that does not contain the key or
            # satisfies the filtering operation, just return the child.
            new_children_with_keys.update({key: child})
      return _set_children(node, new_children_with_keys)

    return node

  # Mimics jax.tree_util.tree_map_with_path(_replace, tree, is_leaf)
  # except that the paths we consider can contain NamedTupleKeys
  _, treedef = jax.tree.flatten(tree, is_leaf=has_any_key)
  tree_leaves_with_path = _tree_leaves_with_named_tuple_path(
      tree, is_leaf=has_any_key
  )
  tree_leaves_with_path = list(zip(*tree_leaves_with_path))
  new_tree = treedef.unflatten(
      _replace(*xs) for xs in zip(*tree_leaves_with_path)
  )
  return new_tree

