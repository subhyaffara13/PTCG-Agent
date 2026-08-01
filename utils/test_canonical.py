
def test_canonical():
    c = [i.canonical for i in (
        x + y < z,
        x + 2 > 3,
        x < 2,
        S(2) > x,
        x**2 > -x/y,
        Gt(3, 2, evaluate=False)
        )]
    assert [i.canonical for i in c] == c
    assert [i.reversed.canonical for i in c] == c
    assert not any(i.lhs.is_Number and not i.rhs.is_Number for i in c)

    c = [i.reversed.func(i.rhs, i.lhs, evaluate=False).canonical for i in c]
    assert [i.canonical for i in c] == c
    assert [i.reversed.canonical for i in c] == c
    assert not any(i.lhs.is_Number and not i.rhs.is_Number for i in c)
    assert Eq(y < x, x > y).canonical is S.true


def test_canonical():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])

