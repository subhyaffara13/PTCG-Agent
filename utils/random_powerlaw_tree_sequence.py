
def random_powerlaw_tree_sequence(n, gamma=3, seed=None, tries=100):
    """Returns a degree sequence for a tree with a power law distribution.

    Parameters
    ----------
    n : int,
        The number of nodes.
    gamma : float
        Exponent of the power law.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    tries : int
        Number of attempts to adjust the sequence to make it a tree.

    Raises
    ------
    NetworkXError
        If no valid sequence is found within the maximum number of
        attempts.

    Notes
    -----
    A trial power law degree sequence is chosen and then elements are
    swapped with new elements from a power law distribution until
    the sequence makes a tree (by checking, for example, that the number of
    edges is one smaller than the number of nodes).

    """
    # get trial sequence
    z = nx.utils.powerlaw_sequence(n, exponent=gamma, seed=seed)
    # round to integer values in the range [0,n]
    zseq = [min(n, max(round(s), 0)) for s in z]

    # another sequence to swap values from
    z = nx.utils.powerlaw_sequence(tries, exponent=gamma, seed=seed)
    # round to integer values in the range [0,n]
    swap = [min(n, max(round(s), 0)) for s in z]

    for _ in swap:
        valid, _ = nx.utils.is_valid_tree_degree_sequence(zseq)
        if valid:
            return zseq
        index = seed.randint(0, n - 1)
        zseq[index] = swap.pop()

    raise nx.NetworkXError(
        f"Exceeded max ({tries}) attempts for a valid tree sequence."
    )

