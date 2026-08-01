
def test__erfs():
    assert _erfs(z).diff(z) == -2/sqrt(S.Pi) + 2*z*_erfs(z)

    assert _erfs(1/z).series(z) == \
        z/sqrt(pi) - z**3/(2*sqrt(pi)) + 3*z**5/(4*sqrt(pi)) + O(z**6)

    assert expand(erf(z).rewrite('tractable').diff(z).rewrite('intractable')) \
        == erf(z).diff(z)
    assert _erfs(z).rewrite("intractable") == (-erf(z) + 1)*exp(z**2)
    raises(ArgumentIndexError, lambda: _erfs(z).fdiff(2))

