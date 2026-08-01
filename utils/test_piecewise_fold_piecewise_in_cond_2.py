
def test_piecewise_fold_piecewise_in_cond_2():
    p1 = Piecewise((cos(x), x < 0), (0, True))
    p2 = Piecewise((0, Eq(p1, 0)), (1 / p1, True))
    p3 = Piecewise(
        (0, (x >= 0) | Eq(cos(x), 0)),
        (1/cos(x), x < 0),
        (zoo, True))  # redundant b/c all x are already covered
    assert(piecewise_fold(p2) == p3)

