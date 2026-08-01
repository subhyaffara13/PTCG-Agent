
def triad_type(G):
    """Returns the sociological triad type for a triad.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph with 3 nodes

    Returns
    -------
    triad_type : str
       A string identifying the triad type

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 1)])
    >>> nx.triad_type(G)
    '030C'
    >>> G.add_edge(1, 3)
    >>> nx.triad_type(G)
    '120C'

    Notes
    -----
    There can be 6 unique edges in a triad (order-3 DiGraph) (so 2^^6=64 unique
    triads given 3 nodes). These 64 triads each display exactly 1 of 16
    topologies of triads (topologies can be permuted). These topologies are
    identified by the following notation:

    {m}{a}{n}{type} (for example: 111D, 210, 102)

    Here:

    {m}     = number of mutual ties (takes 0, 1, 2, 3); a mutual tie is (0,1)
              AND (1,0)
    {a}     = number of asymmetric ties (takes 0, 1, 2, 3); an asymmetric tie
              is (0,1) BUT NOT (1,0) or vice versa
    {n}     = number of null ties (takes 0, 1, 2, 3); a null tie is NEITHER
              (0,1) NOR (1,0)
    {type}  = a letter (takes U, D, C, T) corresponding to up, down, cyclical
              and transitive. This is only used for topologies that can have
              more than one form (eg: 021D and 021U).

    References
    ----------
    .. [1] Snijders, T. (2012). "Transitivity and triads." University of
        Oxford.
        https://web.archive.org/web/20170830032057/http://www.stats.ox.ac.uk/~snijders/Trans_Triads_ha.pdf
    """
    if not is_triad(G):
        raise nx.NetworkXAlgorithmError("G is not a triad (order-3 DiGraph)")
    num_edges = len(G.edges())
    if num_edges == 0:
        return "003"
    elif num_edges == 1:
        return "012"
    elif num_edges == 2:
        e1, e2 = G.edges()
        if set(e1) == set(e2):
            return "102"
        elif e1[0] == e2[0]:
            return "021D"
        elif e1[1] == e2[1]:
            return "021U"
        elif e1[1] == e2[0] or e2[1] == e1[0]:
            return "021C"
    elif num_edges == 3:
        for e1, e2, e3 in permutations(G.edges(), 3):
            if set(e1) == set(e2):
                if e3[0] in e1:
                    return "111U"
                # e3[1] in e1:
                return "111D"
            elif set(e1).symmetric_difference(set(e2)) == set(e3):
                if {e1[0], e2[0], e3[0]} == {e1[0], e2[0], e3[0]} == set(G.nodes()):
                    return "030C"
                # e3 == (e1[0], e2[1]) and e2 == (e1[1], e3[1]):
                return "030T"
    elif num_edges == 4:
        for e1, e2, e3, e4 in permutations(G.edges(), 4):
            if set(e1) == set(e2):
                # identify pair of symmetric edges (which necessarily exists)
                if set(e3) == set(e4):
                    return "201"
                if {e3[0]} == {e4[0]} == set(e3).intersection(set(e4)):
                    return "120D"
                if {e3[1]} == {e4[1]} == set(e3).intersection(set(e4)):
                    return "120U"
                if e3[1] == e4[0]:
                    return "120C"
    elif num_edges == 5:
        return "210"
    elif num_edges == 6:
        return "300"

