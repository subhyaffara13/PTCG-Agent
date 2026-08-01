
def test_SetExpr_Integers():
    assert SetExpr(S.Integers) + 1 == SetExpr(S.Integers)
    assert (SetExpr(S.Integers) + I).dummy_eq(
        SetExpr(ImageSet(Lambda(_d, _d + I), S.Integers)))
    assert SetExpr(S.Integers)*(-1) == SetExpr(S.Integers)
    assert (SetExpr(S.Integers)*2).dummy_eq(
        SetExpr(ImageSet(Lambda(_d, 2*_d), S.Integers)))
    assert (SetExpr(S.Integers)*I).dummy_eq(
        SetExpr(ImageSet(Lambda(_d, I*_d), S.Integers)))
    # issue #18050:
    assert SetExpr(S.Integers)._eval_func(Lambda(x, I*x + 1)).dummy_eq(
        SetExpr(ImageSet(Lambda(_d, I*_d + 1), S.Integers)))
    # needs improvement:
    assert (SetExpr(S.Integers)*I + 1).dummy_eq(
        SetExpr(ImageSet(Lambda(x, x + 1),
        ImageSet(Lambda(_d, _d*I), S.Integers))))

