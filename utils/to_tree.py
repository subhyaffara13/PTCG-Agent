
def to_tree(Z, rd=False):
    """
    Convert a linkage matrix into an easy-to-use tree object.

    The reference to the root `ClusterNode` object is returned (by default).

    Each `ClusterNode` object has a ``left``, ``right``, ``dist``, ``id``,
    and ``count`` attribute. The left and right attributes point to
    ClusterNode objects that were combined to generate the cluster.
    If both are None then the `ClusterNode` object is a leaf node, its count
    must be 1, and its distance is meaningless but set to 0.

    *Note: This function is provided for the convenience of the library
    user. ClusterNodes are not used as input to any of the functions in this
    library.*

    Parameters
    ----------
    Z : ndarray
        The linkage matrix in proper form (see the `linkage`
        function documentation).
    rd : bool, optional
        When False (default), a reference to the root `ClusterNode` object is
        returned.  Otherwise, a tuple ``(r, d)`` is returned. ``r`` is a
        reference to the root node while ``d`` is a list of `ClusterNode`
        objects - one per original entry in the linkage matrix plus entries
        for all clustering steps. If a cluster id is
        less than the number of samples ``n`` in the data that the linkage
        matrix describes, then it corresponds to a singleton cluster (leaf
        node).
        See `linkage` for more information on the assignment of cluster ids
        to clusters.

    Returns
    -------
    tree : ClusterNode or tuple (ClusterNode, list of ClusterNode)
        If ``rd`` is False, a `ClusterNode`.
        If ``rd`` is True, a list of length ``2*n - 1``, with ``n`` the number
        of samples.  See the description of `rd` above for more details.

    See Also
    --------
    linkage, is_valid_linkage, ClusterNode

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.cluster import hierarchy
    >>> rng = np.random.default_rng()
    >>> x = rng.random((5, 2))
    >>> Z = hierarchy.linkage(x)
    >>> hierarchy.to_tree(Z)
    <scipy.cluster.hierarchy.ClusterNode object at ...
    >>> rootnode, nodelist = hierarchy.to_tree(Z, rd=True)
    >>> rootnode
    <scipy.cluster.hierarchy.ClusterNode object at ...
    >>> len(nodelist)
    9

    """
    xp = array_namespace(Z)
    Z = _asarray(Z, order='C', xp=xp)
    _is_valid_linkage(Z, throw=True, name='Z', materialize=True, xp=xp)

    # Number of original objects is equal to the number of rows plus 1.
    n = Z.shape[0] + 1

    # Create a list full of None's to store the node objects
    d = [None] * (n * 2 - 1)

    # Create the nodes corresponding to the n original objects.
    for i in range(0, n):
        d[i] = ClusterNode(i)

    nd = None

    for i in range(Z.shape[0]):
        row = Z[i, :]

        fi = _int_floor(row[0], xp)
        fj = _int_floor(row[1], xp)
        if fi > i + n:
            raise ValueError('Corrupt matrix Z. Index to derivative cluster '
                              f'is used before it is formed. See row {fi}, '
                              'column 0')
        if fj > i + n:
            raise ValueError('Corrupt matrix Z. Index to derivative cluster '
                              f'is used before it is formed. See row {fj}, '
                              'column 1')

        nd = ClusterNode(i + n, d[fi], d[fj], row[2])
        #                ^ id   ^ left ^ right ^ dist
        if row[3] != nd.count:
            raise ValueError(f'Corrupt matrix Z. The count Z[{i},3] is '
                              'incorrect.')
        d[n + i] = nd

    if rd:
        return (nd, d)
    else:
        return nd


def to_tree(
  tree,
  /,
  *,
  prefix: tp.Any = Missing,
  split_fn: tp.Callable[
    [graphlib.SplitContext, KeyPath, Prefix, Leaf], tp.Any
  ] = default_split_fn,
  map_non_graph_nodes: bool = False,
  ctxtag: tp.Hashable | None = None,
  check_aliasing: bool = True,
) -> tp.Any:
  if prefix is Missing or prefix is None:
    # fast path, no need for prefix broadcasting or consistent aliasing checks
    with graphlib.split_context(ctxtag) as split_ctx:
      return jax.tree.map(
        lambda x: split_fn(split_ctx, (), prefix, x)
        if map_non_graph_nodes
        or graphlib.is_graph_node(x)
        or isinstance(x, variablelib.Variable)
        else x,
        tree,
        is_leaf=lambda x: isinstance(x, variablelib.Variable)
        or graphlib.is_graph_node(x),
      )
  leaf_prefixes = broadcast_prefix(
    prefix,
    tree,
    prefix_is_leaf=lambda x: x is None
    or isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x),
    tree_is_leaf=lambda x: isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x),
  )
  leaf_keys, treedef = jax.tree_util.tree_flatten_with_path(
    tree,
    is_leaf=lambda x: isinstance(x, variablelib.Variable)
    or graphlib.is_graph_node(x),
  )

  assert len(leaf_keys) == len(leaf_prefixes)
  leaves_out = []
  node_prefixes: dict[int, list[tuple[PathParts, tp.Any]]] = {}

  with graphlib.split_context(ctxtag) as split_ctx:
    for (keypath, leaf), leaf_prefix in zip(leaf_keys, leaf_prefixes):
      if graphlib.is_graph_node(leaf) or isinstance(leaf, variablelib.Variable):
        if check_aliasing:
          check_consistent_aliasing(
            leaf, leaf_prefix, node_prefixes=node_prefixes
          )
        tree_node = split_fn(split_ctx, keypath, leaf_prefix, leaf)
        leaves_out.append(tree_node)
      else:
        if map_non_graph_nodes:
          leaf = split_fn(split_ctx, keypath, leaf_prefix, leaf)
        leaves_out.append(leaf)

  pytree_out = jax.tree.unflatten(treedef, leaves_out)
  return pytree_out

