
def register_pytree_with_keys(
    nodetype: type[T],
    flatten_with_keys: Callable[[T], tuple[Iterable[KeyLeafPair], _AuxData]],
    unflatten_func: Callable[[_AuxData, Iterable[Any]], T],
    flatten_func: None | (Callable[[T], tuple[Iterable[Any], _AuxData]]) = None,
):
  """Extends the set of types that are considered internal nodes in pytrees.

  This is a more powerful alternative to ``register_pytree_node`` that allows
  you to access each pytree leaf's key path when flattening and tree-mapping.

  Args:
    nodetype: a Python type to treat as an internal pytree node.
    flatten_with_keys: a function to be used during flattening, taking a value
      of type ``nodetype`` and returning a pair, with (1) an iterable for tuples
      of each key path and its child, and (2) some hashable auxiliary data to be
      stored in the treedef and to be passed to the ``unflatten_func``.
    unflatten_func: a function taking two arguments: the auxiliary data that was
      returned by ``flatten_func`` and stored in the treedef, and the
      unflattened children. The function should return an instance of
      ``nodetype``.
    flatten_func: an optional function similar to ``flatten_with_keys``, but
      returns only children and auxiliary data. It must return the children
      in the same order as ``flatten_with_keys``, and return the same aux data.
      This argument is optional and only needed for faster traversal when
      calling functions without keys like ``tree_map`` and ``tree_flatten``.

  Examples:
    First we'll define a custom type:

    >>> class MyContainer:
    ...   def __init__(self, size):
    ...     self.x = jnp.zeros(size)
    ...     self.y = jnp.ones(size)
    ...     self.size = size

    Now register it using a key-aware flatten function:

    >>> from jax.tree_util import register_pytree_with_keys_class, GetAttrKey
    >>> def flatten_with_keys(obj):
    ...   children = [(GetAttrKey('x'), obj.x),
    ...               (GetAttrKey('y'), obj.y)]  # children must contain arrays & pytrees
    ...   aux_data = (obj.size,)  # aux_data must contain static, hashable data.
    ...   return children, aux_data
    ...
    >>> def unflatten(aux_data, children):
    ...   # Here we avoid `__init__` because it has extra logic we don't require:
    ...   obj = object.__new__(MyContainer)
    ...   obj.x, obj.y = children
    ...   obj.size, = aux_data
    ...   return obj
    ...
    >>> jax.tree_util.register_pytree_node(MyContainer, flatten_with_keys, unflatten)

    Now this can be used with functions like :func:`~jax.tree_util.tree_flatten_with_path`:

    >>> m = MyContainer(4)
    >>> leaves, treedef = jax.tree_util.tree_flatten_with_path(m)
  """
  if not flatten_func:
    def flatten_func_impl(tree):
      key_children, treedef = flatten_with_keys(tree)
      return [c for _, c in key_children], treedef
    flatten_func = flatten_func_impl

  register_pytree_node(
      nodetype, flatten_func, unflatten_func, flatten_with_keys
  )

