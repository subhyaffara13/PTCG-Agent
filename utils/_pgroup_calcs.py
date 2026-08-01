
def _pgroup_calcs():
    """Return the permutation groups for each of the polyhedra and the face
    definitions: tetrahedron, cube, octahedron, dodecahedron, icosahedron,
    tetrahedron_faces, cube_faces, octahedron_faces, dodecahedron_faces,
    icosahedron_faces

    Explanation
    ===========

    (This author did not find and did not know of a better way to do it though
    there likely is such a way.)

    Although only 2 permutations are needed for a polyhedron in order to
    generate all the possible orientations, a group of permutations is
    provided instead. A set of permutations is called a "group" if::

    a*b = c (for any pair of permutations in the group, a and b, their
    product, c, is in the group)

    a*(b*c) = (a*b)*c (for any 3 permutations in the group associativity holds)

    there is an identity permutation, I, such that I*a = a*I for all elements
    in the group

    a*b = I (the inverse of each permutation is also in the group)

    None of the polyhedron groups defined follow these definitions of a group.
    Instead, they are selected to contain those permutations whose powers
    alone will construct all orientations of the polyhedron, i.e. for
    permutations ``a``, ``b``, etc... in the group, ``a, a**2, ..., a**o_a``,
    ``b, b**2, ..., b**o_b``, etc... (where ``o_i`` is the order of
    permutation ``i``) generate all permutations of the polyhedron instead of
    mixed products like ``a*b``, ``a*b**2``, etc....

    Note that for a polyhedron with n vertices, the valid permutations of the
    vertices exclude those that do not maintain its faces. e.g. the
    permutation BCDE of a square's four corners, ABCD, is a valid
    permutation while CBDE is not (because this would twist the square).

    Examples
    ========

    The is_group checks for: closure, the presence of the Identity permutation,
    and the presence of the inverse for each of the elements in the group. This
    confirms that none of the polyhedra are true groups:

    >>> from sympy.combinatorics.polyhedron import (
    ... tetrahedron, cube, octahedron, dodecahedron, icosahedron)
    ...
    >>> polyhedra = (tetrahedron, cube, octahedron, dodecahedron, icosahedron)
    >>> [h.pgroup.is_group for h in polyhedra]
    ...
    [True, True, True, True, True]

    Although tests in polyhedron's test suite check that powers of the
    permutations in the groups generate all permutations of the vertices
    of the polyhedron, here we also demonstrate the powers of the given
    permutations create a complete group for the tetrahedron:

    >>> from sympy.combinatorics import Permutation, PermutationGroup
    >>> for h in polyhedra[:1]:
    ...     G = h.pgroup
    ...     perms = set()
    ...     for g in G:
    ...         for e in range(g.order()):
    ...             p = tuple((g**e).array_form)
    ...             perms.add(p)
    ...
    ...     perms = [Permutation(p) for p in perms]
    ...     assert PermutationGroup(perms).is_group

    In addition to doing the above, the tests in the suite confirm that the
    faces are all present after the application of each permutation.

    References
    ==========

    .. [1] https://dogschool.tripod.com/trianglegroup.html

    """
    def _pgroup_of_double(polyh, ordered_faces, pgroup):
        n = len(ordered_faces[0])
        # the vertices of the double which sits inside a give polyhedron
        # can be found by tracking the faces of the outer polyhedron.
        # A map between face and the vertex of the double is made so that
        # after rotation the position of the vertices can be located
        fmap = dict(zip(ordered_faces,
                        range(len(ordered_faces))))
        flat_faces = flatten(ordered_faces)
        new_pgroup = []
        for p in pgroup:
            h = polyh.copy()
            h.rotate(p)
            c = h.corners
            # reorder corners in the order they should appear when
            # enumerating the faces
            reorder = unflatten([c[j] for j in flat_faces], n)
            # make them canonical
            reorder = [tuple(map(as_int,
                       minlex(f, directed=False)))
                       for f in reorder]
            # map face to vertex: the resulting list of vertices are the
            # permutation that we seek for the double
            new_pgroup.append(Perm([fmap[f] for f in reorder]))
        return new_pgroup

    tetrahedron_faces = [
        (0, 1, 2), (0, 2, 3), (0, 3, 1),  # upper 3
        (1, 2, 3),  # bottom
    ]

    # cw from top
    #
    _t_pgroup = [
        Perm([[1, 2, 3], [0]]),  # cw from top
        Perm([[0, 1, 2], [3]]),  # cw from front face
        Perm([[0, 3, 2], [1]]),  # cw from back right face
        Perm([[0, 3, 1], [2]]),  # cw from back left face
        Perm([[0, 1], [2, 3]]),  # through front left edge
        Perm([[0, 2], [1, 3]]),  # through front right edge
        Perm([[0, 3], [1, 2]]),  # through back edge
    ]

    tetrahedron = Polyhedron(
        range(4),
        tetrahedron_faces,
        _t_pgroup)

    cube_faces = [
        (0, 1, 2, 3),  # upper
        (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (0, 3, 7, 4),  # middle 4
        (4, 5, 6, 7),  # lower
    ]

    # U, D, F, B, L, R = up, down, front, back, left, right
    _c_pgroup = [Perm(p) for p in
        [
        [1, 2, 3, 0, 5, 6, 7, 4],  # cw from top, U
        [4, 0, 3, 7, 5, 1, 2, 6],  # cw from F face
        [4, 5, 1, 0, 7, 6, 2, 3],  # cw from R face

        [1, 0, 4, 5, 2, 3, 7, 6],  # cw through UF edge
        [6, 2, 1, 5, 7, 3, 0, 4],  # cw through UR edge
        [6, 7, 3, 2, 5, 4, 0, 1],  # cw through UB edge
        [3, 7, 4, 0, 2, 6, 5, 1],  # cw through UL edge
        [4, 7, 6, 5, 0, 3, 2, 1],  # cw through FL edge
        [6, 5, 4, 7, 2, 1, 0, 3],  # cw through FR edge

        [0, 3, 7, 4, 1, 2, 6, 5],  # cw through UFL vertex
        [5, 1, 0, 4, 6, 2, 3, 7],  # cw through UFR vertex
        [5, 6, 2, 1, 4, 7, 3, 0],  # cw through UBR vertex
        [7, 4, 0, 3, 6, 5, 1, 2],  # cw through UBL
        ]]

    cube = Polyhedron(
        range(8),
        cube_faces,
        _c_pgroup)

    octahedron_faces = [
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 1, 4),  # top 4
        (1, 2, 5), (2, 3, 5), (3, 4, 5), (1, 4, 5),  # bottom 4
    ]

    octahedron = Polyhedron(
        range(6),
        octahedron_faces,
        _pgroup_of_double(cube, cube_faces, _c_pgroup))

    dodecahedron_faces = [
        (0, 1, 2, 3, 4),  # top
        (0, 1, 6, 10, 5), (1, 2, 7, 11, 6), (2, 3, 8, 12, 7),  # upper 5
        (3, 4, 9, 13, 8), (0, 4, 9, 14, 5),
        (5, 10, 16, 15, 14), (6, 10, 16, 17, 11), (7, 11, 17, 18,
          12),  # lower 5
        (8, 12, 18, 19, 13), (9, 13, 19, 15, 14),
        (15, 16, 17, 18, 19)  # bottom
    ]

    def _string_to_perm(s):
        rv = [Perm(range(20))]
        p = None
        for si in s:
            if si not in '01':
                count = int(si) - 1
            else:
                count = 1
                if si == '0':
                    p = _f0
                elif si == '1':
                    p = _f1
            rv.extend([p]*count)
        return Perm.rmul(*rv)

    # top face cw
    _f0 = Perm([
        1, 2, 3, 4, 0, 6, 7, 8, 9, 5, 11,
        12, 13, 14, 10, 16, 17, 18, 19, 15])
    # front face cw
    _f1 = Perm([
        5, 0, 4, 9, 14, 10, 1, 3, 13, 15,
        6, 2, 8, 19, 16, 17, 11, 7, 12, 18])
    # the strings below, like 0104 are shorthand for F0*F1*F0**4 and are
    # the remaining 4 face rotations, 15 edge permutations, and the
    # 10 vertex rotations.
    _dodeca_pgroup = [_f0, _f1] + [_string_to_perm(s) for s in '''
    0104 140 014 0410
    010 1403 03104 04103 102
    120 1304 01303 021302 03130
    0412041 041204103 04120410 041204104 041204102
    10 01 1402 0140 04102 0412 1204 1302 0130 03120'''.strip().split()]

    dodecahedron = Polyhedron(
        range(20),
        dodecahedron_faces,
        _dodeca_pgroup)

    icosahedron_faces = [
        (0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 5), (0, 1, 5),
        (1, 6, 7), (1, 2, 7), (2, 7, 8), (2, 3, 8), (3, 8, 9),
        (3, 4, 9), (4, 9, 10), (4, 5, 10), (5, 6, 10), (1, 5, 6),
        (6, 7, 11), (7, 8, 11), (8, 9, 11), (9, 10, 11), (6, 10, 11)]

    icosahedron = Polyhedron(
        range(12),
        icosahedron_faces,
        _pgroup_of_double(
            dodecahedron, dodecahedron_faces, _dodeca_pgroup))

    return (tetrahedron, cube, octahedron, dodecahedron, icosahedron,
        tetrahedron_faces, cube_faces, octahedron_faces,
        dodecahedron_faces, icosahedron_faces)

