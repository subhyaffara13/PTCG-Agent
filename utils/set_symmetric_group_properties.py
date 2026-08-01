
def set_symmetric_group_properties(G, n, degree):
    """Set known properties of a symmetric group. """
    if n < 3:
        G._is_abelian = True
        G._is_nilpotent = True
    else:
        G._is_abelian = False
        G._is_nilpotent = False
    if n < 5:
        G._is_solvable = True
    else:
        G._is_solvable = False
    G._degree = degree
    G._is_transitive = True
    G._is_dihedral = (n in [2, 3])  # cf Landau's func and Stirling's approx

