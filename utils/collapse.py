import math


def collapse(iterable, base_type=None, levels=None):
    """Flatten an iterable with multiple levels of nesting (e.g., a list of
    lists of tuples) into non-iterable types.

        >>> iterable = [(1, 2), ([3, 4], [[5], [6]])]
        >>> list(collapse(iterable))
        [1, 2, 3, 4, 5, 6]

    Binary and text strings are not considered iterable and
    will not be collapsed.

    To avoid collapsing other types, specify *base_type*:

        >>> iterable = ['ab', ('cd', 'ef'), ['gh', 'ij']]
        >>> list(collapse(iterable, base_type=tuple))
        ['ab', ('cd', 'ef'), 'gh', 'ij']

    Specify *levels* to stop flattening after a certain level:

    >>> iterable = [('a', ['b']), ('c', ['d'])]
    >>> list(collapse(iterable))  # Fully flattened
    ['a', 'b', 'c', 'd']
    >>> list(collapse(iterable, levels=1))  # Only one level flattened
    ['a', ['b'], 'c', ['d']]

    """
    stack = deque()
    # Add our first node group, treat the iterable as a single node
    stack.appendleft((0, repeat(iterable, 1)))

    while stack:
        node_group = stack.popleft()
        level, nodes = node_group

        # Check if beyond max level
        if levels is not None and level > levels:
            yield from nodes
            continue

        for node in nodes:
            # Check if done iterating
            if isinstance(node, (str, bytes)) or (
                (base_type is not None) and isinstance(node, base_type)
            ):
                yield node
            # Otherwise try to create child nodes
            else:
                try:
                    tree = iter(node)
                except TypeError:
                    yield node
                else:
                    # Save our current location
                    stack.appendleft(node_group)
                    # Append the new child node
                    stack.appendleft((level + 1, tree))
                    # Break to process child node
                    break


def collapse(G, grouped_nodes):
    """Collapses each group of nodes into a single node.

    This is similar to condensation, but works on undirected graphs.

    Parameters
    ----------
    G : NetworkX Graph

    grouped_nodes:  list or generator
       Grouping of nodes to collapse. The grouping must be disjoint.
       If grouped_nodes are strongly_connected_components then this is
       equivalent to :func:`condensation`.

    Returns
    -------
    C : NetworkX Graph
       The collapsed graph C of G with respect to the node grouping.  The node
       labels are integers corresponding to the index of the component in the
       list of grouped_nodes.  C has a graph attribute named 'mapping' with a
       dictionary mapping the original nodes to the nodes in C to which they
       belong.  Each node in C also has a node attribute 'members' with the set
       of original nodes in G that form the group that the node in C
       represents.

    Examples
    --------
    >>> # Collapses a graph using disjoint groups, but not necessarily connected
    >>> G = nx.Graph([(1, 0), (2, 3), (3, 1), (3, 4), (4, 5), (5, 6), (5, 7)])
    >>> G.add_node("A")
    >>> grouped_nodes = [{0, 1, 2, 3}, {5, 6, 7}]
    >>> C = collapse(G, grouped_nodes)
    >>> members = nx.get_node_attributes(C, "members")
    >>> sorted(members.keys())
    [0, 1, 2, 3]
    >>> member_values = set(map(frozenset, members.values()))
    >>> assert {0, 1, 2, 3} in member_values
    >>> assert {4} in member_values
    >>> assert {5, 6, 7} in member_values
    >>> assert {"A"} in member_values
    """
    mapping = {}
    members = {}
    C = G.__class__()
    i = 0  # required if G is empty
    remaining = set(G.nodes())
    for i, group in enumerate(grouped_nodes):
        group = set(group)
        assert remaining.issuperset(group), (
            "grouped nodes must exist in G and be disjoint"
        )
        remaining.difference_update(group)
        members[i] = group
        mapping.update((n, i) for n in group)
    # remaining nodes are in their own group
    for i, node in enumerate(remaining, start=i + 1):
        group = {node}
        members[i] = group
        mapping.update((n, i) for n in group)
    number_of_groups = i + 1
    C.add_nodes_from(range(number_of_groups))
    C.add_edges_from(
        (mapping[u], mapping[v]) for u, v in G.edges() if mapping[u] != mapping[v]
    )
    # Add a list of members (ie original nodes) to each node (ie scc) in C.
    nx.set_node_attributes(C, name="members", values=members)
    # Add mapping dict as graph attribute
    C.graph["mapping"] = mapping
    return C


def collapse(operand: Array, start_dimension: int,
             stop_dimension: int | None = None) -> Array:
  """Collapses dimensions of an array into a single dimension.

  For example, if ``operand`` is an array with shape ``[2, 3, 4]``,
  ``collapse(operand, 0, 2).shape == [6, 4]``. The elements of the collapsed
  dimension are laid out major-to-minor, i.e., with the lowest-numbered
  dimension as the slowest varying dimension.

  Args:
    operand: an input array.
    start_dimension: the start of the dimensions to collapse (inclusive).
    stop_dimension: the end of the dimensions to collapse (exclusive). Pass None
      to collapse all the dimensions after start.

  Returns:
    An array where dimensions ``[start_dimension, stop_dimension)`` have been
    collapsed (raveled) into a single dimension.
  """
  lo, hi, _ = slice(start_dimension, stop_dimension).indices(len(operand.shape))
  if hi < lo:
    raise ValueError(f"Invalid dimension range passed to collapse: {operand.shape}"
                     f"[{start_dimension}:{stop_dimension}]")
  size = math.prod(operand.shape[lo:hi])
  new_shape = operand.shape[:lo] + (size,) + operand.shape[hi:]
  return reshape(operand, new_shape)


def collapse(name: str = '', *, expanded: bool = False) -> Iterator[None]:
  """Capture all outputs and display it in a collapsible block.

  Args:
    name: Name of the collapsible section.
    expanded: If `True`, the section is expanded by default.

  Yields:
    None
  """
  import ipywidgets  # pylint: disable=g-import-not-at-top

  out = ipywidgets.Output()
  accordion = ipywidgets.Accordion(children=[out])
  accordion.set_title(0, name)
  if expanded:
    accordion.selected_index = 0
  else:
    accordion.selected_index = None
  IPython.display.display(accordion)
  with out:
    try:
      yield
    except BaseException as e:  # BaseException to support KeyboardInterupt
      # ipywidgets.Output erase exceptions, so we save it and reraise it after
      # the scope.
      exc = e  # pylint: disable=unused-variable
      raise
    else:
      exc = None
  if exc is not None:
    raise exc  # pylint: disable=g-doc-exception

