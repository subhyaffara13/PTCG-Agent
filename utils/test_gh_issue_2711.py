
def test_gh_issue_2711():
    x = Symbol('x')
    f = meijerg(((), ()), ((0,), ()), x)
    a = Wild('a')
    b = Wild('b')

    assert f.find(a) == {(S.Zero,), ((), ()), ((S.Zero,), ()), x, S.Zero,
                             (), meijerg(((), ()), ((S.Zero,), ()), x)}
    assert f.find(a + b) == \
        {meijerg(((), ()), ((S.Zero,), ()), x), x, S.Zero}
    assert f.find(a**2) == {meijerg(((), ()), ((S.Zero,), ()), x), x}

