
def check_subgraphs_connected(
    subgraph1: SourcePartition, subgraph2: SourcePartition
) -> bool:
    """
    Given two subgraphs A and B (in the form of a list of nodes), checks if
    A has nodes connecting to at least one node in B -- aka there exists a node
    in B that uses a node in A (not the other way around).
    """

    for node in reversed(subgraph1.nodes):
        for user in node.users:
            if user in subgraph2.nodes:
                return True
    return False

