
def test_issue_21481():
    b, e = symbols('b e')
    C = Piecewise(
        (2,
        ((b > 1) & (e > 0)) |
        ((b > 0) & (b < 1) & (e < 0)) |
        ((e >= 2) & (b < -1) & Eq(Mod(e, 2), 0)) |
        ((e <= -2) & (b > -1) & (b < 0) & Eq(Mod(e, 2), 0))),
        (S.Half,
        ((b > 1) & (e < 0)) |
        ((b > 0) & (e > 0) & (b < 1)) |
        ((e <= -2) & (b < -1) & Eq(Mod(e, 2), 0)) |
        ((e >= 2) & (b > -1) & (b < 0) & Eq(Mod(e, 2), 0))),
        (-S.Half,
        Eq(Mod(e, 2), 1) &
        (((e <= -1) & (b < -1)) | ((e >= 1) & (b > -1) & (b < 0)))),
        (-2,
        ((e >= 1) & (b < -1) & Eq(Mod(e, 2), 1)) |
        ((e <= -1) & (b > -1) & (b < 0) & Eq(Mod(e, 2), 1)))
    )
    A = Piecewise(
        (1, Eq(b, 1) | Eq(e, 0) | (Eq(b, -1) & Eq(Mod(e, 2), 0))),
        (0, Eq(b, 0) & (e > 0)),
        (-1, Eq(b, -1) & Eq(Mod(e, 2), 1)),
        (C, Eq(im(b), 0) & Eq(im(e), 0))
    )

    B = piecewise_fold(A)
    sa = A.simplify()
    sb = B.simplify()
    v = (-2, -1, -S.Half, 0, S.Half, 1, 2)
    for i in v:
        for j in v:
            r = {b:i, e:j}
            ok = [k.xreplace(r) for k in (A, B, sa, sb)]
            assert len(set(ok)) == 1

