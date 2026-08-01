
def is_valid_tree_degree_sequence(degree_sequence):
    """Check if a degree sequence is valid for a tree.

    Two conditions must be met for a degree sequence to be valid for a tree:

    1. The number of nodes must be one more than the number of edges.
    2. The degree sequence must be trivial or have only strictly positive
       node degrees.

    Parameters
    ----------
    degree_sequence : iterable
        Iterable of node degrees.

    Returns
    -------
    bool
        Whether the degree sequence is valid for a tree.
    str
        Reason for invalidity, or dummy string if valid.
    """
    seq = list(degree_sequence)
    number_of_nodes = len(seq)
    twice_number_of_edges = sum(seq)

    if 2 * number_of_nodes - twice_number_of_edges != 2:
        return False, "tree must have one more node than number of edges"
    elif seq != [0] and any(d <= 0 for d in seq):
        return False, "nontrivial tree must have strictly positive node degrees"
    return True, ""

