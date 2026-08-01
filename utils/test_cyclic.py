
def test_cyclic():
    F, x, y = free_group("x, y")
    f = FpGroup(F, [x*y, x**-1*y**-1*x*y*x])
    assert f.is_cyclic
    f = FpGroup(F, [x*y, x*y**-1])
    assert f.is_cyclic
    f = FpGroup(F, [x**4, y**2, x*y*x**-1*y])
    assert not f.is_cyclic


def test_cyclic():
    G = SymmetricGroup(2)
    assert G.is_cyclic
    G = AbelianGroup(3, 7)
    assert G.is_cyclic
    G = AbelianGroup(7, 7)
    assert not G.is_cyclic
    G = AlternatingGroup(3)
    assert G.is_cyclic
    G = AlternatingGroup(4)
    assert not G.is_cyclic

    # Order less than 6
    G = PermutationGroup(Permutation(0, 1, 2), Permutation(0, 2, 1))
    assert G.is_cyclic
    G = PermutationGroup(
        Permutation(0, 1, 2, 3),
        Permutation(0, 2)(1, 3)
    )
    assert G.is_cyclic
    G = PermutationGroup(
        Permutation(3),
        Permutation(0, 1)(2, 3),
        Permutation(0, 2)(1, 3),
        Permutation(0, 3)(1, 2)
    )
    assert G.is_cyclic is False

    # Order 15
    G = PermutationGroup(
        Permutation(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
        Permutation(0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13)
    )
    assert G.is_cyclic

    # Distinct prime orders
    assert PermutationGroup._distinct_primes_lemma([3, 5]) is True
    assert PermutationGroup._distinct_primes_lemma([5, 7]) is True
    assert PermutationGroup._distinct_primes_lemma([2, 3]) is None
    assert PermutationGroup._distinct_primes_lemma([3, 5, 7]) is None
    assert PermutationGroup._distinct_primes_lemma([5, 7, 13]) is True

    G = PermutationGroup(
        Permutation(0, 1, 2, 3),
        Permutation(0, 2)(1, 3))
    assert G.is_cyclic
    assert G._is_abelian

    # Non-abelian and therefore not cyclic
    G = PermutationGroup(*SymmetricGroup(3).generators)
    assert G.is_cyclic is False

    # Abelian and cyclic
    G = PermutationGroup(
        Permutation(0, 1, 2, 3),
        Permutation(4, 5, 6)
    )
    assert G.is_cyclic

    # Abelian but not cyclic
    G = PermutationGroup(
        Permutation(0, 1),
        Permutation(2, 3),
        Permutation(4, 5, 6)
    )
    assert G.is_cyclic is False


def test_cyclic(n, axis):
    """Test that the cyclic group correctly fixes the rotations of a
    pyramid."""
    P = _generate_pyramid(n, axis='XYZ'.index(axis))
    for g in Rotation.create_group(f"C{n}", axis=axis):
        assert _calculate_rmsd(P, g.apply(P)) < TOL

