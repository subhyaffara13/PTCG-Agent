
def node_to_part_ID_dict(partition):
    """
    Creates a dictionary that maps each item in each part to the index of
    the part to which it belongs.

    Parameters
    ----------
    partition: collections.abc.Sequence[collections.abc.Iterable]
        As returned by :func:`make_partition`.

    Returns
    -------
    dict
    """
    return {node: ID for ID, part in enumerate(partition) for node in part}

