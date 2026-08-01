
def _community(G, u, community):
    """Get the community of the given node."""
    node_u = G.nodes[u]
    try:
        return node_u[community]
    except KeyError as err:
        raise nx.NetworkXAlgorithmError(
            f"No community information available for Node {u}"
        ) from err

