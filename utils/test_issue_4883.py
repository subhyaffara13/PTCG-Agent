
def test_issue_4883():
    a = Wild('a')
    x = Symbol('x')

    e = [i**2 for i in (x - 2, 2 - x)]
    p = [i**2 for i in (x - a, a- x)]
    for eq in e:
        for pat in p:
            assert eq.match(pat) == {a: 2}

