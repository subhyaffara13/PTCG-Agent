
def test_sympy__combinatorics__polyhedron__Polyhedron():
    from sympy.combinatorics.permutations import Permutation
    from sympy.combinatorics.polyhedron import Polyhedron
    from sympy.abc import w, x, y, z
    pgroup = [Permutation([[0, 1, 2], [3]]),
              Permutation([[0, 1, 3], [2]]),
              Permutation([[0, 2, 3], [1]]),
              Permutation([[1, 2, 3], [0]]),
              Permutation([[0, 1], [2, 3]]),
              Permutation([[0, 2], [1, 3]]),
              Permutation([[0, 3], [1, 2]]),
              Permutation([[0, 1, 2, 3]])]
    corners = [w, x, y, z]
    faces = [(w, x, y), (w, y, z), (w, z, x), (x, y, z)]
    assert _test_args(Polyhedron(corners, faces, pgroup))

