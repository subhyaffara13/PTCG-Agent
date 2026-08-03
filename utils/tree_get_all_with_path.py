from typing import Any, Callable, Optional

def tree_get_all_with_path(
    tree: base.PyTree,
    key: Any,
    filtering: Optional[Callable[[_KeyPath, Any], bool]] = None,
) -> list[tuple[_KeyPath, Any]]:
  # pylint: disable=line-too-long
  r"""Extract values of a pytree matching a given key.

  Search in a pytree ``tree`` for a specific ``key`` (which can be a key
  from a dictionary, a field from a NamedTuple or the name of a NamedTuple).

  That key/field ``key`` may appear more than once in ``tree``. So this function
  returns a list of all values corresponding to ``key`` with the path to
  that value. The path is a sequence of ``KeyEntry`` that can be transformed in
  readable format using :func:`jax.tree_util.keystr`, see the example below.

  Args:
    tree: tree to search in.
    key: keyword or field to search in tree for.
    filtering: optional callable to further filter values in tree that match the
      key. ``filtering(path: Key_Path, value: Any) -> bool: ...`` takes as
      arguments both the path to the value (as returned by
      :func:`optax.tree_utils.tree_get_all_with_path`) and the value that match
      the given key.

  Returns:
    values_with_path
      list of tuples where each tuple is of the form
      (``path_to_value``, ``value``). Here ``value`` is one entry of the tree
      that corresponds to the ``key``, and ``path_to_value`` is a tuple of
      `KeyEntry` that is a tuple of :class:`jax.tree_util.DictKey`,
      :class:`jax.tree_util.FlattenedIndexKey`,
      :class:`jax.tree_util.GetAttrKey`,
      :class:`jax.tree_util.SequenceKey`, or
      :class:`optax.tree_utils.NamedTupleKey`.

  Examples:

    Basic usage

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> solver = optax.inject_hyperparams(optax.sgd)(
      ...   learning_rate=lambda count: 1/(count+1)
      ... )
      >>> state = solver.init(params)
      >>> found_values_with_path = optax.tree_utils.tree_get_all_with_path(
      ...   state, 'learning_rate'
      ... )
      >>> print(
      ... *[(jax.tree_util.keystr(p), v) for p, v in found_values_with_path],
      ... sep="\n",
      ... )
      ("InjectStatefulHyperparamsState.hyperparams['learning_rate']", Array(1., dtype=float32))
      ("InjectStatefulHyperparamsState.hyperparams_states['learning_rate']", WrappedScheduleState(count=Array(0, dtype=int32)))

    Usage with a filtering operation

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> solver = optax.inject_hyperparams(optax.sgd)(
      ...   learning_rate=lambda count: 1/(count+1)
      ... )
      >>> state = solver.init(params)
      >>> filtering = lambda path, value: isinstance(value, tuple)
      >>> found_values_with_path = optax.tree_utils.tree_get_all_with_path(
      ...   state, 'learning_rate', filtering
      ... )
      >>> print(
      ... *[(jax.tree_util.keystr(p), v) for p, v in found_values_with_path],
      ... sep="\n",
      ... )
      ("InjectStatefulHyperparamsState.hyperparams_states['learning_rate']", WrappedScheduleState(count=Array(0, dtype=int32)))

  .. seealso:: :func:`optax.tree_utils.tree_get`,
    :func:`optax.tree_utils.tree_set`

  .. versionadded:: 0.2.2
  """  # noqa: E501
  # pylint: enable=line-too-long
  found_values_with_path = _tree_get_all_with_path(tree, key)
  if filtering:
    found_values_with_path = [
        (path, value)
        for path, value in found_values_with_path
        if filtering(path, value)
    ]
  return found_values_with_path

