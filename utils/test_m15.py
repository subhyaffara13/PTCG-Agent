
def test_M15():
    n = Dummy('n')
    got = solveset(sin(x) - S.Half)
    assert any(got.dummy_eq(i) for i in (
        Union(ImageSet(Lambda(n, 2*n*pi + pi/6), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi*R(5, 6)), S.Integers)),
        Union(ImageSet(Lambda(n, 2*n*pi + pi*R(5, 6)), S.Integers),
        ImageSet(Lambda(n, 2*n*pi + pi/6), S.Integers))))

