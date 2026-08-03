import functools
from typing import Optional

def tree_dtype(
    tree: base.ArrayTree, mixed_dtype_handler: Optional[str] = None
) -> jax.typing.DTypeLike:
  """Fetch dtype of tree.

  If the tree is empty, returns the default dtype of JAX arrays.

  Args:
    tree: the tree to fetch the dtype of.
    mixed_dtype_handler: how to handle mixed dtypes in the tree.  - If
      ``mixed_dtype_handler=None``, returns the common dtype of the leaves of
      the tree if it exists, otherwise raises an error. - If
      ``mixed_dtype_handler='promote'``, promotes the dtypes of the leaves of
      the tree to a common promoted dtype using :func:`jax.numpy.promote_types`.
      - If ``mixed_dtype_handler='highest'`` or
      ``mixed_dtype_handler='lowest'``, returns the highest/lowest dtype of the
      leaves of the tree. We consider a partial ordering of dtypes as ``dtype1
      <= dtype2`` if ``dtype1`` is promoted to ``dtype2``, that is, if
      ``jax.numpy.promote_types(dtype1, dtype2) == dtype2``. Since some dtypes
      cannot be promoted to one another, this is not a total ordering, and the
      'highest' or 'lowest' options may not be applicable. These options will
      throw an error if the dtypes of the leaves of the tree cannot be promoted
      to one another.

  Returns:
    the dtype of the tree.

  Raises:
    ValueError: If ``mixed_dtype_handler`` is set to ``None`` and multiple
      dtypes are found in the tree.
    ValueError: If ``mixed_dtype_handler`` is set to  ``'highest'`` or
      ``'lowest'`` and some leaves' dtypes in the tree cannot be promoted to one
      another.

  Examples:
    >>> import jax.numpy as jnp
    >>> import optax
    >>> tree = {'a': {'b': jnp.array(1.0, dtype=jnp.float32)},
    ...         'c': jnp.array(2.0, dtype=jnp.float32)}
    >>> optax.tree_utils.tree_dtype(tree)
    dtype('float32')
    >>> tree = {'a': {'b': jnp.array(1.0, dtype=jnp.float16)},
    ...         'c': jnp.array(2.0, dtype=jnp.float32)}
    >>> optax.tree_utils.tree_dtype(tree, 'lowest')
    dtype('float16')
    >>> optax.tree_utils.tree_dtype(tree, 'highest')
    dtype('float32')
    >>> tree = {'a': {'b': jnp.array(1.0, dtype=jnp.int32)},
    ...         'c': jnp.array(2.0, dtype=jnp.uint32)}
    >>> # optax.tree_utils.tree_dtype(tree, 'highest')
    >>> # -> will throw an error because int32 and uint32
    >>> # cannot be promoted to one another.
    >>> optax.tree_utils.tree_dtype(tree, 'promote')
    dtype('int32')

  .. seealso:: :func:`jax.numpy.promote_types`,
    `Type promotion semantics in JAX
    <https://jax.readthedocs.io/en/latest/type_promotion.html#type-promotion>`_

  .. versionadded:: 0.2.4
  """
  leaves = jax.tree.leaves(tree)
  if not leaves:
    # If the tree is empty, we return the default dtype as given by JAX on
    # empty lists.
    return jnp.asarray(leaves).dtype
  if mixed_dtype_handler is None:
    dtype = jnp.asarray(leaves[0]).dtype
    _tree_assert_all_dtypes_equal(tree, dtype)
    return dtype
  if mixed_dtype_handler == 'promote':
    promoted_dtype = functools.reduce(
        jnp.promote_types, [jnp.asarray(x).dtype for x in leaves]
    )
    return promoted_dtype
  if mixed_dtype_handler == 'highest':
    highest_dtype = functools.reduce(
        _higher_dtype, [jnp.asarray(x).dtype for x in leaves]
    )
    return highest_dtype
  if mixed_dtype_handler == 'lowest':
    lowest_dtype = functools.reduce(
        _lower_dtype, [jnp.asarray(x).dtype for x in leaves]
    )
    return lowest_dtype
  raise ValueError(
      f'Invalid value for {mixed_dtype_handler=}, possible values are: None,'
      ' "promote", "highest", "lowest".'
  )

