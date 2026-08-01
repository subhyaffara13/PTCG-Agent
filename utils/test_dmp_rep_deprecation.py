
def test_DMP_rep_deprecation():
    f = DMP([1, 2, 3], ZZ)

    with warns_deprecated_sympy():
        assert f.rep == [1, 2, 3]

