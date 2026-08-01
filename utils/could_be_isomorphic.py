
def could_be_isomorphic(G1, G2, *, properties="dtc"):
    """Returns False if graphs are definitely not isomorphic.
    True does NOT guarantee isomorphism.

    Parameters
    ----------
    G1, G2 : graphs
       The two graphs `G1` and `G2` must be the same type.

    properties : str, default="dct"
       Determines which properties of the graph are checked. Each character
       indicates a particular property as follows:

       - if ``"d"`` in `properties`: degree of each node
       - if ``"t"`` in `properties`: number of triangles for each node
       - if ``"c"`` in `properties`: number of maximal cliques for each node

       Unrecognized characters are ignored. The default is ``"dtc"``, which
       compares the sequence of ``(degree, num_triangles, num_cliques)`` properties
       between `G1` and `G2`. Generally, ``properties="dt"`` would be faster, and
       ``properties="d"`` faster still. See Notes for additional details on
       property selection.

    Returns
    -------
    bool
       A Boolean value representing whether `G1` could be isomorphic with `G2`
       according to the specified `properties`.

    Notes
    -----
    The triangle sequence contains the number of triangles each node is part of.
    The clique sequence contains for each node the number of maximal cliques
    involving that node.

    Some properties are faster to compute than others. And there are other
    properties we could include and don't. But of the three properties listed here,
    comparing the degree distributions is the fastest. The "triangles" property
    is slower (and also a stricter version of "could") and the "maximal cliques"
    property is slower still, but usually faster than doing a full isomorphism
    check.
    """

    # Check global properties
    if G1.order() != G2.order():
        return False

    properties_to_check = set(properties)
    G1_props, G2_props = [], []

    def _properties_consistent():
        # Ravel the properties into a table with # nodes rows and # properties columns
        G1_ptable = [tuple(p[n] for p in G1_props) for n in G1]
        G2_ptable = [tuple(p[n] for p in G2_props) for n in G2]

        return sorted(G1_ptable) == sorted(G2_ptable)

    # The property table is built and checked as each individual property is
    # added. The reason for this is the building/checking the property table
    # is in general much faster than computing the properties, making it
    # worthwhile to check multiple times to enable early termination when
    # a subset of properties don't match

    # Degree sequence
    if "d" in properties_to_check:
        G1_props.append(G1.degree())
        G2_props.append(G2.degree())
        if not _properties_consistent():
            return False
    # Sequence of triangles per node
    if "t" in properties_to_check:
        G1_props.append(nx.triangles(G1))
        G2_props.append(nx.triangles(G2))
        if not _properties_consistent():
            return False
    # Sequence of maximal cliques per node
    if "c" in properties_to_check:
        G1_props.append(Counter(itertools.chain.from_iterable(nx.find_cliques(G1))))
        G2_props.append(Counter(itertools.chain.from_iterable(nx.find_cliques(G2))))
        if not _properties_consistent():
            return False

    # All checked conditions passed
    return True

