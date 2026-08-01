
def test_NZQRC_unions():
    # check that all trivial number set unions are simplified:
    nbrsets = (S.Naturals, S.Naturals0, S.Integers, S.Rationals,
        S.Reals, S.Complexes)
    unions = (Union(a, b) for a in nbrsets for b in nbrsets)
    assert all(u.is_Union is False for u in unions)

