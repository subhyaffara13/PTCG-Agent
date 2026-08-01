
def test_ufunc_support():
    f = Function('f')
    g = Function('g')
    x = IndexedBase('x')
    y = IndexedBase('y')
    i, j = Idx('i'), Idx('j')
    a = symbols('a')

    assert get_indices(f(x[i])) == ({i}, {})
    assert get_indices(f(x[i], y[j])) == ({i, j}, {})
    assert get_indices(f(y[i])*g(x[i])) == (set(), {})
    assert get_indices(f(a, x[i])) == ({i}, {})
    assert get_indices(f(a, y[i], x[j])*g(x[i])) == ({j}, {})
    assert get_indices(g(f(x[i]))) == ({i}, {})

    assert get_contraction_structure(f(x[i])) == {None: {f(x[i])}}
    assert get_contraction_structure(
        f(y[i])*g(x[i])) == {(i,): {f(y[i])*g(x[i])}}
    assert get_contraction_structure(
        f(y[i])*g(f(x[i]))) == {(i,): {f(y[i])*g(f(x[i]))}}
    assert get_contraction_structure(
        f(x[j], y[i])*g(x[i])) == {(i,): {f(x[j], y[i])*g(x[i])}}

