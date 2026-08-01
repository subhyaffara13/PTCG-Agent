
def _galois_group_degree_3(T, max_tries=30, randomize=False):
    r"""
    Compute the Galois group of a polynomial of degree 3.

    Explanation
    ===========

    Uses Prop 6.3.5 of [1].

    """
    from sympy.combinatorics.galois import S3TransitiveSubgroups
    return ((S3TransitiveSubgroups.A3, True) if has_square_disc(T)
            else (S3TransitiveSubgroups.S3, False))

