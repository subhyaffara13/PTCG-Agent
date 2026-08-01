
def test_issue_11538():
    assert solve(x + E) == [-E]
    assert solve(x**2 + E) == [-I*sqrt(E), I*sqrt(E)]
    assert solve(x**3 + 2*E) == [
        -cbrt(2 * E),
        cbrt(2)*cbrt(E)/2 - cbrt(2)*sqrt(3)*I*cbrt(E)/2,
        cbrt(2)*cbrt(E)/2 + cbrt(2)*sqrt(3)*I*cbrt(E)/2]
    assert solve([x + 4, y + E], x, y) == {x: -4, y: -E}
    assert solve([x**2 + 4, y + E], x, y) == [
        (-2*I, -E), (2*I, -E)]

    e1 = x - y**3 + 4
    e2 = x + y + 4 + 4 * E
    assert len(solve([e1, e2], x, y)) == 3


def test_issue_11538():
    for n in [E, pi, Catalan]:
        assert construct_domain(n)[0] == ZZ[n]
        assert construct_domain(x + n)[0] == ZZ[x, n]
    assert construct_domain(GoldenRatio)[0] == EX
    assert construct_domain(x + GoldenRatio)[0] == EX

