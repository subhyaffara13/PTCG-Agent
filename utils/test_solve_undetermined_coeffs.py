
def test_solve_undetermined_coeffs():
    assert solve_undetermined_coeffs(
        a*x**2 + b*x**2 + b*x + 2*c*x + c + 1, [a, b, c], x
        ) == {a: -2, b: 2, c: -1}
    # Test that rational functions work
    assert solve_undetermined_coeffs(a/x + b/(x + 1)
        - (2*x + 1)/(x**2 + x), [a, b], x) == {a: 1, b: 1}
    # Test cancellation in rational functions
    assert solve_undetermined_coeffs(
        ((c + 1)*a*x**2 + (c + 1)*b*x**2 +
        (c + 1)*b*x + (c + 1)*2*c*x + (c + 1)**2)/(c + 1),
        [a, b, c], x) == \
        {a: -2, b: 2, c: -1}
    # multivariate
    X, Y, Z = y, x**y, y*x**y
    eq = a*X + b*Y + c*Z - X - 2*Y - 3*Z
    coeffs = a, b, c
    syms = x, y
    assert solve_undetermined_coeffs(eq, coeffs) == {
        a: 1, b: 2, c: 3}
    assert solve_undetermined_coeffs(eq, coeffs, syms) == {
        a: 1, b: 2, c: 3}
    assert solve_undetermined_coeffs(eq, coeffs, *syms) == {
        a: 1, b: 2, c: 3}
    # check output format
    assert solve_undetermined_coeffs(a*x + a - 2, [a]) == []
    assert solve_undetermined_coeffs(a**2*x - 4*x, [a]) == [
        {a: -2}, {a: 2}]
    assert solve_undetermined_coeffs(0, [a]) == []
    assert solve_undetermined_coeffs(0, [a], dict=True) == []
    assert solve_undetermined_coeffs(0, [a], set=True) == ([], {})
    assert solve_undetermined_coeffs(1, [a]) == []
    abeq = a*x - 2*x + b - 3
    s = {b, a}
    assert solve_undetermined_coeffs(abeq, s, x) == {a: 2, b: 3}
    assert solve_undetermined_coeffs(abeq, s, x, set=True) == ([a, b], {(2, 3)})
    assert solve_undetermined_coeffs(sin(a*x) - sin(2*x), (a,)) is None
    assert solve_undetermined_coeffs(a*x + b*x - 2*x, (a, b)) == {a: 2 - b}

