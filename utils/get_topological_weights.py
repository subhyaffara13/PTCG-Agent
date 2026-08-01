
def get_topological_weights(
    graph: DirectedGraph[str | None], requirement_keys: set[str]
) -> dict[str | None, int]:
    """Assign weights to each node based on how "deep" they are.

    This implementation may change at any point in the future without prior
    notice.

    We first simplify the dependency graph by pruning any leaves and giving them
    the highest weight: a package without any dependencies should be installed
    first. This is done again and again in the same way, giving ever less weight
    to the newly found leaves. The loop stops when no leaves are left: all
    remaining packages have at least one dependency left in the graph.

    Then we continue with the remaining graph, by taking the length for the
    longest path to any node from root, ignoring any paths that contain a single
    node twice (i.e. cycles). This is done through a depth-first search through
    the graph, while keeping track of the path to the node.

    Cycles in the graph result would result in node being revisited while also
    being on its own path. In this case, take no action. This helps ensure we
    don't get stuck in a cycle.

    When assigning weight, the longer path (i.e. larger length) is preferred.

    We are only interested in the weights of packages that are in the
    requirement_keys.
    """
    path: set[str | None] = set()
    weights: dict[str | None, list[int]] = {}

    def visit(node: str | None) -> None:
        if node in path:
            # We hit a cycle, so we'll break it here.
            return

        # The walk is exponential and for pathologically connected graphs (which
        # are the ones most likely to contain cycles in the first place) it can
        # take until the heat-death of the universe. To counter this we limit
        # the number of attempts to visit (i.e. traverse through) any given
        # node. We choose a value here which gives decent enough coverage for
        # fairly well behaved graphs, and still limits the walk complexity to be
        # linear in nature.
        cur_weights = weights.get(node, [])
        if len(cur_weights) >= 5:
            return

        # Time to visit the children!
        path.add(node)
        for child in graph.iter_children(node):
            visit(child)
        path.remove(node)

        if node not in requirement_keys:
            return

        cur_weights.append(len(path))
        weights[node] = cur_weights

    # Simplify the graph, pruning leaves that have no dependencies. This is
    # needed for large graphs (say over 200 packages) because the `visit`
    # function is slower for large/densely connected graphs, taking minutes.
    # See https://github.com/pypa/pip/issues/10557
    # We repeat the pruning step until we have no more leaves to remove.
    while True:
        leaves = set()
        for key in graph:
            if key is None:
                continue
            for _child in graph.iter_children(key):
                # This means we have at least one child
                break
            else:
                # No child.
                leaves.add(key)
        if not leaves:
            # We are done simplifying.
            break
        # Calculate the weight for the leaves.
        weight = len(graph) - 1
        for leaf in leaves:
            if leaf not in requirement_keys:
                continue
            weights[leaf] = [weight]
        # Remove the leaves from the graph, making it simpler.
        for leaf in leaves:
            graph.remove(leaf)

    # Visit the remaining graph, this will only have nodes to handle if the
    # graph had a cycle in it, which the pruning step above could not handle.
    # `None` is guaranteed to be the root node by resolvelib.
    visit(None)

    # Sanity check: all requirement keys should be in the weights,
    # and no other keys should be in the weights.
    difference = set(weights.keys()).difference(requirement_keys)
    assert not difference, difference

    # Now give back all the weights, choosing the largest ones from what we
    # accumulated.
    return {node: max(wgts) for (node, wgts) in weights.items()}

