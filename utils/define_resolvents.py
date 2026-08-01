
def define_resolvents():
    """Define all the resolvents for polys T of degree 4 through 6. """
    from sympy.combinatorics.galois import PGL2F5
    from sympy.combinatorics.permutations import Permutation

    R4, X4 = xring("X0,X1,X2,X3", ZZ, lex)
    X = X4

    # The one resolvent used in `_galois_group_degree_4_lookup()`:
    F40 = X[0]*X[1]**2 + X[1]*X[2]**2 + X[2]*X[3]**2 + X[3]*X[0]**2
    s40 = [
        Permutation(3),
        Permutation(3)(0, 1),
        Permutation(3)(0, 2),
        Permutation(3)(0, 3),
        Permutation(3)(1, 2),
        Permutation(3)(2, 3),
    ]

    # First resolvent used in `_galois_group_degree_4_root_approx()`:
    F41 = X[0]*X[2] + X[1]*X[3]
    s41 = [
        Permutation(3),
        Permutation(3)(0, 1),
        Permutation(3)(0, 3)
    ]

    R5, X5 = xring("X0,X1,X2,X3,X4", ZZ, lex)
    X = X5

    # First resolvent used in `_galois_group_degree_5_hybrid()`,
    # and only one used in `_galois_group_degree_5_lookup_ext_factor()`:
    F51 = (  X[0]**2*(X[1]*X[4] + X[2]*X[3])
           + X[1]**2*(X[2]*X[0] + X[3]*X[4])
           + X[2]**2*(X[3]*X[1] + X[4]*X[0])
           + X[3]**2*(X[4]*X[2] + X[0]*X[1])
           + X[4]**2*(X[0]*X[3] + X[1]*X[2]))
    s51 = [
        Permutation(4),
        Permutation(4)(0, 1),
        Permutation(4)(0, 2),
        Permutation(4)(0, 3),
        Permutation(4)(0, 4),
        Permutation(4)(1, 4)
    ]

    R6, X6 = xring("X0,X1,X2,X3,X4,X5", ZZ, lex)
    X = X6

    # First resolvent used in `_galois_group_degree_6_lookup()`:
    H = PGL2F5()
    term0 = X[0]**2*X[5]**2*(X[1]*X[4] + X[2]*X[3])
    terms = {term0.compose(list(zip(X, s(X)))) for s in H.elements}
    F61 = sum(terms)
    s61 = [Permutation(5)] + [Permutation(5)(0, n) for n in range(1, 6)]

    # Second resolvent used in `_galois_group_degree_6_lookup()`:
    F62 = X[0]*X[1]*X[2] + X[3]*X[4]*X[5]
    s62 = [Permutation(5)] + [
        Permutation(5)(i, j + 3) for i in range(3) for j in range(3)
    ]

    return {
        (4, 0): (F40, X4, s40),
        (4, 1): (F41, X4, s41),
        (5, 1): (F51, X5, s51),
        (6, 1): (F61, X6, s61),
        (6, 2): (F62, X6, s62),
    }

