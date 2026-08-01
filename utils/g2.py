
def G2():
    # Now we shift all the weights by -10.
    # Should not affect optimal arborescence, but does affect optimal branching.
    Garr = G_array.copy()
    Garr[np.nonzero(Garr)] -= 10
    G = nx.from_numpy_array(Garr, create_using=nx.MultiDiGraph)
    return G

