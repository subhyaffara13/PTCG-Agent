
def tree_get(
    tree: base.PyTree,
    key: Any,
    default: Optional[Any] = None,
    filtering: Optional[Callable[[_KeyPath, Any], bool]] = None,
) -> Any:
  # pylint: disable=line-too-long
  """Extract a value from a pytree matching a given key.

  Search in the ``tree`` for a specific ``key`` (which can be a key
  from a dictionary, a field from a NamedTuple or the name of a NamedTuple).

  If the ``tree`` does not contain ``key`` returns ``default``.

  Raises a ``KeyError`` if multiple values of ``key`` are found in ``tree``.

  Generally, you may first get all pairs ``(path_to_value, value)`` for a given
  ``key`` using :func:`optax.tree_utils.tree_get_all_with_path`. You may then
  define a filtering operation
  ``filtering(path: Key_Path, value: Any) -> bool: ...`` that enables you to
  select the specific values you wanted to fetch by looking at the type of the
  value, or looking at the path to that value.
  Note that contrarily to the paths returned by
  :func:`jax.tree_util.tree_leaves_with_path` the paths analyzed by the
  filtering operation in :func:`optax.tree_utils.tree_get_all_with_path`,
  :func:`optax.tree_utils.tree_get`, or :func:`optax.tree_utils.tree_set` detail
  the names of the named tuples considered in the path. Concretely, if the value
  considered is in the attribute ``key`` of a named tuple called
  ``MyNamedTuple`` the last element of the path will be a
  :class:`optax.tree_utils.NamedTupleKey` containing both ``name=key`` and
  ``tuple_name='MyNamedTuple'``. That way you may distinguish between identical
  values in different named tuples (arising for example when chaining
  transformations in optax). See the last example below.

  Args:
    tree: tree to search in.
    key: keyword or field to search in ``tree`` for.
    default: default value to return if ``key`` is not found in ``tree``.
    filtering: optional callable to further filter values in ``tree`` that match
      the ``key``. ``filtering(path: Key_Path, value: Any) -> bool: ...`` takes
      as arguments both the path to the value (as returned by
      :func:`optax.tree_utils.tree_get_all_with_path`) and the value that match
      the given key.

  Returns:
    value
      value in ``tree`` matching the given ``key``. If none are
      found return ``default`` value. If multiple are found raises an error.

  Raises:
    KeyError: If multiple values of ``key`` are found in ``tree``.

  Examples:

    Basic usage

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.adam(learning_rate=1.)
      >>> state = opt.init(params)
      >>> count = optax.tree_utils.tree_get(state, 'count')
      >>> print(count)
      0

    Usage with a filtering operation

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.inject_hyperparams(optax.sgd)(
      ...   learning_rate=lambda count: 1/(count+1)
      ... )
      >>> state = opt.init(params)
      >>> filtering = lambda path, value: isinstance(value, jnp.ndarray)
      >>> lr = optax.tree_utils.tree_get(
      ...   state, 'learning_rate', filtering=filtering
      ... )
      >>> print(lr)
      1.0

    Extracting a named tuple by its name

      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.chain(
      ...     optax.add_noise(1.0, 0.9, key=0),
      ...     optax.scale_by_adam()
      ... )
      >>> state = opt.init(params)
      >>> noise_state = optax.tree_utils.tree_get(state, 'AddNoiseState')
      >>> print(noise_state)
      AddNoiseState(count=Array(0, dtype=int32), rng_key=Array((), dtype=key<fry>) overlaying:
      [0 0])

    Differentiating between two values by the name of their named tuples.

      >>> import jax.numpy as jnp
      >>> import optax
      >>> params = jnp.array([1., 2., 3.])
      >>> opt = optax.chain(
      ...   optax.add_noise(1.0, 0.9, key=0),
      ...   optax.scale_by_adam()
      ... )

  .. seealso:: :func:`optax.tree_utils.tree_get_all_with_path`,
    :func:`optax.tree_utils.tree_set`

  .. versionadded:: 0.2.2
  """  # noqa: E501
  # pylint: enable=line-too-long
  found_values_with_path = tree_get_all_with_path(
      tree, key, filtering=filtering
  )
  if len(found_values_with_path) > 1:
    raise KeyError(f"Found multiple values for '{key}' in {tree}.")
  if not found_values_with_path:
    return default
  return found_values_with_path[0][1]

